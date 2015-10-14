import copy


class VertexWrapper(object):
    def __init__(self, impl):
        self._dict = copy.deepcopy(impl)

    @property
    def vertex_id(self):
        return self._dict['id']

    @property
    def vertex_label(self):
        return self._dict['label']

    @property
    def properties(self):
        return copy.deepcopy(self._dict['properties'])

    def get_all_property_values(self, key):
        values_list = self._dict[u'properties'].get(key, [])
        return [v['value'] for v in values_list]

    def __getattr__(self, key):
        values_list = self._dict[u'properties'].get(key, None)
        if values_list is None or not values_list:
            return None
        return values_list[0]['value']
    
    def __repr__(self):
        return 'VertexWrapper(%r)' % self._dict


class EdgeWrapper(object):
    def __init__(self, impl):
        self._dict = copy.deepcopy(impl)

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

    @property
    def edge_label(self):
        return self._dict['label']
    
    @property
    def edge_id(self):
        return self._dict['id']

    def __getattr__(self, key):
        return self._dict[u'properties'].get(key, None)

    def __repr__(self):
        return 'EdgeWrapper(%r)' % self._dict

def get_wrapper(elem):
    if isinstance(elem, dict):
        type = elem.get('type', None)
        if type == 'vertex':
            return VertexWrapper(elem)
        if type == 'edge':
            return EdgeWrapper(elem)
    return elem
