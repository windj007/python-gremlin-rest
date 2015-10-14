graph.traversal().E(edge_id).each { it -> it.remove() }
graph.tx().commit()