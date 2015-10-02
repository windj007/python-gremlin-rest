import os, glob
from gremlinpy.gremlin import Gremlin
from pyarc import ClientBase


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
        super(RexsterClient, self).__init__(base_url,
                                            add_headers = { 'Content-Type' : 'application/json; charset=utf-8' },
                                            async = async)
        self.scripts = {}
        self.refresh_scripts(os.path.join(os.path.dirname(__file__), 'scripts'))
        print repr(self.do_req)

    def __getattr__(self, script_name):
        assert script_name in self.scripts, 'Trying to call unknown script %s' % script_name
        return ScriptCaller(self, script_name)

    def gremlin(self):
        return ExecutableGremlin(self)

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
                               label = label,
                               properties = props)

    ############################## Overrides ##########################
    def _do_req_base(self, *args, **kwargs):
        return _ItemGetter(_ItemGetter(super(RexsterClient, self)._do_req_base(*args, **kwargs),
                                       'result'),
                           'data')
