graph.traversal().V(vertex_id).each { it.remove() }
graph.tx().commit()