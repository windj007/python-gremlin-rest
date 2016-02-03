import os, glob
from gremlinpy.gremlin import Gremlin
from pyarc import ClientBase
from gremlin_rest.wrappers import get_wrapper, VertexWrapper, EdgeWrapper

__ALL__ = ['GremlinClient']


class _ItemGetter(object):
    def __init__(self, base_future, attrib, default = None):
        self.base_future = base_future
        self.attrib = attrib
        self.default = None

    def get(self):
        base_res = self.base_future.get()
        try:
            return base_res.get(self.attrib, self.default)
        except:
            return self.default


class ListWithFirst(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def first(self, default = None):
        if len(self) == 0:
            return default
        return self[0]


class _WrapperAssigner(object):
    def __init__(self, base_future):
        self.base_future = base_future

    def get(self):
        base_res = self.base_future.get()
        try:
            return ListWithFirst(map(get_wrapper, base_res))
        except:
            return base_res


class ScriptCaller(object):
    def __init__(self, client, name):
        self.client = client
        self.script_name = name

    def __call__(self, **kwargs):
        return self.client.run_script(self.script_name, **kwargs)


class ExecutableGremlin(Gremlin):
    def __init__(self, client, *args, **kwargs):
        super(ExecutableGremlin, self).__init__(*args, **kwargs)
        self.client = client

    def run(self):
        return self.client.run_script(str(self), **self.bound_params)


class GremlinClient(ClientBase):
    def __init__(self, base_url, async = False):
        super(GremlinClient, self).__init__(base_url,
                                            add_headers = { 'Content-Type' : 'application/json; charset=utf-8' },
                                            async = async)
        self.scripts = {}
        self.refresh_scripts(os.path.join(os.path.dirname(__file__), 'scripts'))

    def __getattr__(self, script_name):
        assert script_name in self.scripts, 'Trying to call unknown script %s' % script_name
        return ScriptCaller(self, script_name)

    def gremlin(self):
        return ExecutableGremlin(self, graph_variable = 'graph')

    def V(self, arg = None):
        if not arg is None:
            if issubclass(type(arg), VertexWrapper):
                arg = arg.vertex_id
            return self.gremlin().traversal().V(arg)
        return self.gremlin().traversal().V()

    def E(self, arg = None):
        if not arg is None:
            if issubclass(type(arg), EdgeWrapper):
                arg = arg.edge_id
            return self.gremlin().traversal().E(arg)
        return self.gremlin().traversal().E()
    
    def refresh_scripts(self, dirname):
        for f in glob.glob(os.path.join(dirname, "*.groovy")):
            self.load_script(f)

    def load_script(self, filename):
        if not os.path.isfile(filename):
            return
        script_name = os.path.splitext(os.path.basename(filename))[0]
        with open(filename, 'r') as f:
            self.scripts[script_name] = f.read()

    def run_script(self, script_code_or_name, **params):
        return self.post('/', payload = {
                                        "bindings" : params,
                                        "gremlin" : self.scripts.get(script_code_or_name,
                                                                     script_code_or_name)
                                        })

    def upsert_vertex_custom_id(self, id_prop, id_value, label = None, **props):
        return self.run_script('upsert_vertex_custom_id',
                               id_prop = id_prop,
                               id_value = id_value,
                               _label = label,
                               properties = props)

    def addVertex(self, label = None, **properties):
        return self.run_script('addVertex',
                               _label = label,
                               properties = properties)

    ############################## Overrides ##########################
    def _do_req_base(self, *args, **kwargs):
        base_res = super(GremlinClient, self)._do_req_base(*args, **kwargs)
        data = _ItemGetter(_ItemGetter(base_res, 'result'), 'data')
        return _WrapperAssigner(data)
