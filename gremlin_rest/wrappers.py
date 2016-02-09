import copy


class BaseWrapper(object):
    def __init__(self, impl, client):
        self._dict = copy.deepcopy(impl)
        self.client = client

    @property
    def id(self):
        return self._dict['id']

    @property
    def label(self):
        return self._dict['label']

    @property
    def properties(self):
        return copy.deepcopy(self._dict['properties'])

    def get_all_property_values(self, key):
        values_list = self._dict['properties'].get(key, [])
        return [v['value'] for v in values_list]

    def __getattr__(self, key):
        values_list = self._dict['properties'].get(key, None)
        if values_list is None or not values_list:
            return None
        return values_list[0]['value']
    
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__,
                               self._dict,
                               self.client)


class VertexWrapper(BaseWrapper):
    def traverse(self):
        return self.client.V(self)


class EdgeWrapper(object):
    @property
    def in_v_id(self):
        return self._dict['inV']

    @property
    def in_v_label(self):
        return self._dict['inVLabel']

    @property
    def out_v_id(self):
        return self._dict['outV']

    @property
    def out_v_label(self):
        return self._dict['outVLabel']

    def traverse(self):
        return self.client.E(self)


class WrapperMapping(object):
    def __init__(self, client):
        self.client = client
        self._fallback = {
                          'edge' : EdgeWrapper,
                          'vertex' : VertexWrapper
                          }
        self._mapping = {
                         'edge' : { },
                         'vertex' : { }
                         }

    def register_wrapper(self, type, label, func):
        self._mapping[type][label] = func

    def __call__(self, elem):
        if isinstance(elem, dict):
            type, label = elem.get('type', None), elem.get('label', None)
            wrapper_func = self._mapping[type].get(label, self._fallback[type])
            return wrapper_func(elem, client)
        return elem
