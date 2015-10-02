def vs = null, v = null;
def created = false;
if (label != null)
	vs = g.query().has('label', label).has(id_prop, id_value).vertices();
else
	vs = g.query().has(id_prop, id_value).vertices();
if (vs.count() > 0)
	v = vs.get(0);
else {
	if (label != null)
		v = g.addVertexWithLabel(label);
	else
		v = g.addVertex();
	v.setProperty(id_prop, id_value);
	created = true;
};
properties.each { k, val ->
	v.setProperty(k, val);
};
g.commit();

[v, created]