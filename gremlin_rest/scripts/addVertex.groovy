if (_label == null)
	v = graph.addVertex();
else
	v = graph.addVertex(T.label, _label);
properties.each { key, val ->
	v.property(key, val)
}
graph.tx().commit()
v