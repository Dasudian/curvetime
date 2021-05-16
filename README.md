# CurveTime Blockchain

A Blockchain that organically orchestrates Proof of Work and AI model Training on one platform, optimizting the resource usage for intense computation.

## How it is implemented? And how it works?
Please read the [A Blockchain model for AI computation](https://www.dasudian.com/curvetime/paper/curvetime-paper.html) to understand its principle. 

## Instructions to run

1. Install CouchDB
```sh
curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
echo "deb https://apache.bintray.com/couchdb-deb focal main" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install couchdb
```
2. Configure CouchDB
```
sudo vi /opt/couchdb/etc/default.ini
max_document_size = 80000000;
```

3. Clone the project,

```sh
$ git clone https://github.com/dasudian/curvetime
```

4. Install the dependencies,

```sh
$ cd curvetime
$ pip install -r requirements.txt
```

5. Start a blockchain node server

```sh
$ Python3 manage.py runserver 0.0.0.0:8000
```

One instance of our blockchain node is now up and running at port 8000.


Run the application on a different terminal session/server,

```sh
$ Python3 manage.py runserver 0.0.0.0:8001
```

The application should be up and running at [http://localhost:8001](http://localhost:8001).



To play around by spinning off multiple custom nodes, use the `register_with/` endpoint to register a new node. 

Here's a sample scenario that you might wanna try,

```sh
# already running
$ python3 manage.py runserver 0.0.0.0:8000 &
# spinning up new nodes
$ python3 manage.py runserver 0.0.0.0:8001 &
$ python3 manage.py runserver 0.0.0.0:8002 &
```

You can use the following cURL requests to register the nodes at port `8001` and `8002` with the already running `8000`.

```sh
curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

```sh
curl -X POST \
  http://127.0.0.1:8002/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

This will make the node at port 8000 aware of the nodes at port 8001 and 8002, and make the newer nodes sync the chain with the node 8000, so that they are able to actively participate in the mining process post registration.

To update the node with which the frontend application syncs (default is localhost port 8000), change `CONNECTED_NODE_ADDRESS` field in the [settings](app/settings.py) file.

Once you do all this, you can run the application, create transactions, and once you mine the transactions, all the nodes in the network will update the chain. The chain of the nodes can also be inspected by inovking `/bc/chain` endpoint using cURL.

```sh
$ curl -X GET http://localhost:8001/node/chain
$ curl -X GET http://localhost:8002/node/chain
