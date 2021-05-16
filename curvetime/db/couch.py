import requests
import json
from app.settings import COUCH_SERVER_URL, COUCH_DATABASE


def init_db(db_name=COUCH_DATABASE):
    res = requests.put(COUCH_SERVER_URL + db_name)
    if res.status_code == 201 or res.status_code == 200:
        return True
    else:
        return False


def put(key, value, db=COUCH_DATABASE):
    """
    value: dict type
    """
    value = json.dumps(value)
    res = requests.put(COUCH_SERVER_URL + db + '/' + key, data=value)
    if res.status_code == 201:
        return True
    else:
        return False


def get(key, db=COUCH_DATABASE):
    res = requests.get(COUCH_SERVER_URL + db + '/' + key)
    if res.status_code == 200:
        value = res.json()
        del(value['_id'])
        del(value['_rev'])
        return value
    else:
        return None


def get_withkey(key, db=COUCH_DATABASE):
    res = requests.get(COUCH_SERVER_URL + db + '/' + key)
    if res.status_code == 200:
        value = res.json()
        del(value['_rev'])
        return value
    else:
        return None


def keys(db=COUCH_DATABASE):
    res = requests.get(COUCH_SERVER_URL + db + '/_all_docs')
    if res.status_code == 200:
        value = res.json()
        value = value['rows']
        value = [get_withkey(v['key']) for v in value]
        value = sorted(value, key=lambda key:key['timestamp'])
        value = [v['_id'] for v in value]
        return value
    else:
        return None


def all(db=COUCH_DATABASE):
    res = requests.get(COUCH_SERVER_URL + db + '/_all_docs')
    if res.status_code == 200:
        value = res.json()
        value = value['rows']
        value = [get(v['key']) for v in value]
        return value
    else:
        return None


def replicate_from(remote, db=COUCH_DATABASE):
    headers = {'Content-Type': 'application/json'}
    data = {'source': remote + '/' + db,
            'target': COUCH_SERVER_URL + db}
    res = requests.post(COUCH_SERVER_URL+'/_replicate',
            headers=headers,
            data=json.dumps(data))
    if res.status_code == 200:
        return True
    else:
        return False


def delete(db=COUCH_DATABASE):
    res = requests.delete(COUCH_SERVER_URL + db)
    if res.status_code == 200:
        return True
    else:
        return False
