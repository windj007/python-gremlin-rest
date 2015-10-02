# python-gremlin-rest
A very simple JSON-REST client to TinkerPop 3 Gremlin Server.

Features:
* gremlin expressions
* transparent scripts execution
* synchronous and asynchronous evaluation


# Dependencies
Depends on [pyarc](https://github.com/windj007/pyarc) to communicate with server and on [gremlinpy tp3](https://github.com/emehrkay/gremlinpy/tree/tp3) to build Gremlin expressions. Supports adding custom scripts from files.

# Installation
Unfortunately, currently available only from Github. PyPI package to be done.

    # pip install -U gremlinpy \
        git+https://github.com/windj007/pyarc.git \
        git+https://github.com/windj007/python-gremlin-rest.git

# Examples
## Synchronous mode
```python
from gremlin_rest import GremlinClient
client = GremlinClient('http://172.17.0.29:8182')
print client.gremlin().V().count().run()
# outputs [0]
print client.run_script('g.addV(label, "test", "name", "1")')
# outputs [{u'properties': {u'name': [{u'id': u'17a-3ao-1l1', u'value': u'1'}]}, u'type': u'vertex', u'id': 4272, u'label': u'test'}]
print client.run_script('g.addV(label, "test", prop, val)', prop = 'name', val = 123) 
# outputs [{u'properties': {u'name': [{u'id': u'2dy-6gg-1l1', u'value': 123}]}, u'type': u'vertex', u'id': 8368, u'label': u'test'}]
print client.gremlin().V().count().run()
# outputs [2]
print client.gremlin().V().run()
# outputs [{u'properties': {u'name': [{u'id': u'17a-3ao-1l1', u'value': u'1'}]}, u'type': u'vertex', u'id': 4272, u'label': u'test'}, {u'properties': {u'name': [{u'id': u'2dy-6gg-1l1', u'value': 123}]}, u'type': u'vertex', u'id': 8368, u'label': u'test'}]
```

## Asynchronous mode
```python
from gremlin_rest import GremlinClient, Signature
client = GremlinClient('http://172.17.0.29:8182', async = True)
future = client.run_script('g.V().each { it.remove() }')
print future.get()
# outputs []
print client.gremlin().V().count().run().get()
# outputs [0]
print client.batch([Signature(client.run_script, 'g.addV(label, "test", "name", "1")'),
                    Signature(client.run_script, 'g.addV(label, "test", prop, val)', prop = 'name', val = 123)])
# outputs [[{u'properties': {u'name': [{u'id': u'16t-36w-1l1', u'value': u'1'}]}, u'type': u'vertex', u'id': 4136, u'label': u'test'}], [{u'properties': {u'name': [{u'id': u'16r-36g-1l1', u'value': 123}]}, u'type': u'vertex', u'id': 4120, u'label': u'test'}]]
print client.batch([Signature(client.gremlin().V().count().run),
                    Signature(client.gremlin().V().values('name').run)])
# outputs [[2], [u'1', 123]]
```

## Stored scripts
You can write your scripts in Gremlin-Groovy, save it to a folder, then load and call as if they were usual Python functions.

Useful for complex logic.
```bash
mkdir scripts
cat > scripts/select_vertices.groovy <<EOF
query = g.V()
kwargs.each { k, val ->
    query = query.has(k, val);
};
query.toList()
EOF
```
```python
from gremlin_rest import GremlinClient
client = GremlinClient('http://172.17.0.29:8182')
client.refresh_scripts('./scripts')
client.select_vertices(kwargs = dict(name = 123))
# outputs [{u'id': 4120,
#           u'label': u'test',
#           u'properties': {u'name': [{u'id': u'16r-36g-1l1', u'value': 123}]},
#           u'type': u'vertex'}]
```
# TODO
* tests
* PyPI package
* API cleanup
* ???
