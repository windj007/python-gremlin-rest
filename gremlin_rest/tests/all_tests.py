import unittest
from gremlin_rest import GremlinClient


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = GremlinClient('http://172.17.0.248:8182')

    def tearDown(self):
        for v in self.client.V().run():
            self.client.delete_vertex(vertex_id = v.vertex_id)

    def test_add_vertex(self):
        init_cnt = len(self.client.V().run())
        v = self.client.addVertex(label = "a", a = 123,  b = 'qweq').first()
        print repr(v)
        vs = self.client.V().run()
        print repr(vs)
        self.assertEqual(len(vs) - init_cnt, 1)
        self.client.delete_vertex(vertex_id = v.vertex_id)
        self.assertEqual(len(self.client.V().run()), init_cnt)

    def test_query_vertices(self):
        print 'before', repr(self.client.V().run())
        v1 = self.client.addVertex(a = 123,  b = 'qwe').first()
        v2 = self.client.addVertex(a = 1234,  b = 'qwe').first()
        print 'all', repr(self.client.V().run())
        print '12', repr(self.client.V().has('a', 12).run())
        print '123', repr(self.client.V().has('a', 123).run())
        print '1234', repr(self.client.V().has('a', 1234).run())
        print 'qwe', repr(self.client.V().has('b', 'qwe').run())
        self.assertEqual(len(self.client.V().has('a', 12).run()), 0)
        self.assertEqual(len(self.client.V().has('a', 123).run()), 1)
        self.assertEqual(len(self.client.V().has('a', 1234).run()), 1)
        self.assertEqual(len(self.client.V().has('b', 'qwe').run()), 2)
        self.client.delete_vertex(vertex_id = v1.vertex_id)
        self.client.delete_vertex(vertex_id = v2.vertex_id)

if __name__ == '__main__':
    unittest.main()
