import unittest
from gremlin_rest import RexsterClient


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = RexsterClient('http://localhost:8182', 'graph')

    def tearDown(self):
        for v in self.client.vertices().get():
            self.client.delete_vertex(v['_id']).get()

    def test_add_vertex(self):
        init_cnt = len(self.client.vertices().get())
        v = self.client.create_vertex(a = 123,  b = 'qweq').get()
        print repr(v)
        vs = self.client.vertices().get()
        print repr(vs)
        self.assertEqual(len(vs) - init_cnt, 1)
        self.client.delete_vertex(v['_id']).get()
        self.assertEqual(len(self.client.vertices().get()), init_cnt)

    def test_query_vertices(self):
        print 'before', repr(self.client.vertices().get())
        v1 = self.client.create_vertex(a = 123,  b = 'qwe').get()
        v2 = self.client.create_vertex(a = 1234,  b = 'qwe').get()
        print 'all', repr(self.client.vertices().get())
        print '12', repr(self.client.vertices('a', 12).get())
        print '123', repr(self.client.vertices('a', 123).get())
        print '1234', repr(self.client.vertices('a', 1234).get())
        print 'qwe', repr(self.client.vertices('b', 'qwe'))
        self.assertEqual(len(self.client.vertices('a', 12).get()), 0)
        self.assertEqual(len(self.client.vertices('a', 123).get()), 1)
        self.assertEqual(len(self.client.vertices('a', 1234).get()), 1)
        self.assertEqual(len(self.client.vertices('b', 'qwe').get()), 2)
        self.client.delete_vertex(v1['_id']).get()
        self.client.delete_vertex(v2['_id']).get()
    
    def test_scripts(self):
        script = '''
        qq = 123;
        1 + a + qq'''
        self.assertEqual(self.client.run_script_on_graph(script, a = 22).get()[0], 146)
        self.assertEqual(self.client.run_script_on_graph('[1, 2, a]', a = 22).get(), [1, 2, 22])

if __name__ == '__main__':
    unittest.main()
