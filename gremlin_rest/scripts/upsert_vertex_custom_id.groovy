def v = null;
def created = false;
def v_iter = (_label != null) ?
	  graph.traversal().V().has(_label, id_prop, id_value)
	: graph.traversal().V().has(id_prop, id_value);
if (v_iter.hasNext()) {
	v = v_iter.next();
} else {
	if (_label != null)
		v = graph.addVertex(T.label, _label);
	else
		v = graph.addVertex();
	v.property(id_prop, id_value);
	created = true;
}
properties.each { k, val ->
	v.property(k, val);
}
graph.tx().commit();

[v, created]