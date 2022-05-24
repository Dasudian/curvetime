# CurveTime Blockchain

A Blockchain that organically orchestrates Proof-of-work and AI model Training on one platform, optimizing the resource usage for intense computation.

## How it is implemented? And how it works?
Please read the paper: [Blockchain Framework for AI computation](https://doi.org/10.21203/rs.3.rs-1000746/v1) to understand its principle. 

## Instructions to run
1. Install Prerequisites
```
sudo apt install postgresql postgresql-server-dev-all redis-server python3-dev gcc
```

2. Install CouchDB
```sh
sudo apt update && sudo apt install -y curl apt-transport-https gnupg
curl https://couchdb.apache.org/repo/keys.asc | gpg --dearmor | sudo tee /usr/share/keyrings/couchdb-archive-keyring.gpg >/dev/null 2>&1
source /etc/os-release
echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ ${VERSION_CODENAME} main" \
    | sudo tee /etc/apt/sources.list.d/couchdb.list >/dev/null
sudo apt update
sudo apt install -y couchdb

or refer to: https://docs.couchdb.org/en/latest/install/unix.html#installation-from-source to install CouchDB from source
```
3. Configure CouchDB
```
sudo vi /opt/couchdb/etc/default.ini
max_document_size = 80000000;
systemctl start couchdb.service
systemctl enable couchdb.service
```
4. Clone the project,

```sh
$ git clone https://github.com/dasudian/curvetime
```

5. Install the dependencies,

```sh
$ cd curvetime
$ pip install -r requirements.txt
```

6. Configure app/settings.py
```
...
SECRET_KEY = 'give something here'
JWT_SECRET_KEY = 'give something here'
...
#configure the proper DB connection for your Ai models feeding data if you use Postgresql
PG_DATABASE = os.environ.get("PG_DATABASE") or ''
PG_USER = os.environ.get("PG_USER") or ''
PG_PASSWORD = os.environ.get("PG_PASSWORD") or ''
PG_HOST = os.environ.get("PG_HOST") or '127.0.0.1'
PG_PORT = os.environ.get("PG_PORT") or '5432'
...

# Configure your CouchDB connection here
COUCH_SERVER_URL = 'http://admin:admin@localhost:5984/'
COUCH_DATABASE = 'curvetime'


# Configure your Blockchain Nodes
CONNECTED_NODE_ADDRESS = ['http://localhost:8000']
```

7. (Optional) load the example data (for AI models crunching) to Postgresql
```
sudo su postgres
psql
>CREATE ROLE stockai with login password 'stockai';
>CREATE DATABASE stockai with OWNER stockai;
>\q
exit
sudo vi /etc/postgresql/12/main/pg_hba.conf, adding following line:
"host stockai stockai 127.0.0.1/32 md5"
sudo service postgresql restart
psql -U stockai -h 127.0.0.1 < data/examples/stockai/stockai_scheme.sql
psql -U stockai -h 127.0.0.1
>\COPY stockai_stocks FROM 'data/examples/stockai/stockai_stocks.csv' DELIMITER ',' CSV HEADER;
>\COPY stockai_feature2 FROM 'data/examples/stockai/stockai_feature2.csv' DELIMITER ',' CSV HEADER;
>\q
```

8. Start a blockchain node server

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
  http://127.0.0.1:8001/node/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

```sh
curl -X POST \
  http://127.0.0.1:8002/node/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

This will make the node at port 8000 aware of the nodes at port 8001 and 8002, and make the newer nodes sync the chain with the node 8000, so that they are able to actively participate in the mining process post registration.

To update the node with which the frontend application syncs (default is localhost port 8000), change `CONNECTED_NODE_ADDRESS` field in the [settings](app/settings.py) file.

Once you do all this, you can run the application, create transactions, and once you mine the transactions, all the nodes in the network will update the chain. The chain of the nodes can also be inspected by inovking `/bc/chain` endpoint using cURL.


9. Check the chain information

```sh
$ curl -X GET http://localhost:8001/node/chain
$ curl -X GET http://localhost:8002/node/chain
```


10. Create new data with transaction
```
$ curl -X POST -H"Content-Type:application/json" http://localhost:8001/api/transaction -d 'data_in_json_format'
```

11. Fetch a transaction
```
$ curl http://localhost:8002/api/transaction?hash=xxxxxxxxx
```

## Todo
- Merkel Tree
- Node Discovery
- Channels
- Smart Contract Engine
- Wallet
- AI Models and Environments based on [Gym](https://gym.openai.com)
