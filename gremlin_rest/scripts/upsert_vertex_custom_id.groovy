def v = null;
def created = false;
def v_iter = (label != null) ?
	  graph.traversal().V().has(T.label, label).has(id_prop, id_value)
	: graph.traversal().query().has(id_prop, id_value);
if (v_iter.hasNext())
	v = v_iter.next();
else {
	if (label != null)
		v = graph.addVertex(T.label, label);
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