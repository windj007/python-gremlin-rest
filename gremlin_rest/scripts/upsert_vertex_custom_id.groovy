def v = null;
def created = false;
try {
	if (label != null)
		v = graph.traversal().V().has(T.label, label).has(id_prop, id_value).next();
	else
		v = graph.traversal().query().has(id_prop, id_value).next();
catch (NoSuchElementException) {
}
if (v == null) {
	if (label != null)
		v = graph.addVertex(T.label, label);
	else
		v = graph.addVertex();
	v.property(id_prop, id_value);
	created = true;
};
properties.each { k, val ->
	v.property(k, val);
};
graph.tx().commit();

[v, created]