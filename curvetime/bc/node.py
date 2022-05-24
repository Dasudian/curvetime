import time, json, requests
from rest_framework.views import APIView
from curvetime.utils.utils import util_response
from curvetime.bc.blockchain import Blockchain, Block
from curvetime.utils import ecode

from curvetime.oracle.stocks import *
from curvetime.env.stock_env import *
from curvetime.ai.cnn import *
from curvetime.ai.cnn_agent import *
from curvetime.db import couch



o = StockOracle()
env = StockEnv(o)
model = CNN(env, filepath='data/models/model.h5')
target_model = CNN(env, filepath='data/models/target_model.h5')
agent = Agent(model, target_model, env)
blockchain = Blockchain(agent)
# the address to other participating members of the network
peers = set()



# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
class Transaction(APIView):
    def post(self, request):
        tx_data = request.data
        tx_data["timestamp"] = time.time()

        blockchain.add_new_transaction(tx_data)

        result = sync_mine()
        if not result:
            return util_response(code=ecode.ERROR)

        index = result[0]
        hash = result[1]
        return util_response({'hash': hash,
                          'index': index})


    def get(self, request):
        hash = request.GET.get('hash')
        block = blockchain.fetch_block(hash)
        if not block:
            return util_response(code=ecode.NotFound)
        #data = json.dumps(block.__dict__, sort_keys=True)
        data = json.dumps(block)
        return util_response(data)



# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
class Block(APIView):
    def post(self, request):
        block_data = request.data
        proof = block_data['hash']
        block = block_data['block']
        block = Block(**block)

        added = blockchain.add_block(block, proof)

        if not added:
            return util_response(code=ecode.ERROR)

        return util_response(code=201, data="Block added to the chain")


# endpoint to query unconfirmed transactions
class Pending(APIView):
    def get(self, request):
        return util_response(blockchain.unconfirmed_transactions)





# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
class Chain(APIView):
    def get(self, request):
        chain = blockchain.chain
        data = {"length": len(chain),
            "chain": chain,
            "peers": list(peers)}
        return util_response(data)


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
class Mine(APIView):
    def get(self, request):
        result = blockchain.mine()
        if not result:
            return util_response(code = ecode.NoTransToMine)
        else:
            # Making sure we have the longest chain before announcing to the network
            chain_length = len(blockchain.chain)
            consensus()
            if chain_length == len(blockchain.chain):
                # announce the recently mined block to the network
                last_block_hash = blockchain.last_block_hash
                last_block = blockchain.fetch_block(last_block_hash)
                announce_new_block(last_block_hash, last_block)
            data = {"index": last_block.index,
                    "hash": last_block_hash}
            return util_response(data)


def sync_mine():
    result = blockchain.mine()
    if not result:
        return None
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            last_block_hash = blockchain.last_block_hash
            last_block = blockchain.fetch_block(last_block_hash)
            announce_new_block(last_block_hash, last_block)
        return last_block.index, last_block_hash




# endpoint to add new peers to the network.
class Register(APIView):
    def post(self, request):
        node_address = request.data.get("node_address")
        if not node_address:
            return util_response(code=ecode.ERROR)

        # Add the node to the peer list
        global blockchain
        global peers
        self_peer = request.get_host()
        peers.add(self_peer)
        peers.add(node_address)
        chain = blockchain.chain

        # Return the consensus blockchain to the newly registered node
        # so that he can sync
        data = {'peers': peers, 'chain': chain}
        return util_response(data)


class RegisterWith(APIView):
    def post(self, request):
        """
        Internally calls the `register_node` endpoint to
        register current node with the node specified in the
        request, and sync the blockchain as well as peer data.
        """
        node_address = request.data.get("node_address")
        if not node_address:
            return util_response(code=ecode.ERROR)

        data = {"node_address": request.get_host()}
        headers = {'Content-Type': "application/json"}

        # Make a request to register with remote node and obtain information
        response = requests.post(node_address + "/node/register_node",
                             data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            global blockchain
            global peers
            # update chain and the peers
            data = response.json()['data']
            chain_dump = data['chain']
            blockchain = create_chain_from_dump(chain_dump, node_address)
            peers.update(data['peers'])
            return util_response()
        else:
            # if something goes wrong, pass it on to the API response
            return util_response(code=response.status_code)


def create_chain_from_dump(chain_dump, node_address):
    generated_blockchain = Blockchain(agent)
    generated_blockchain.chain = chain_dump
    #uncomment following line if deploying nodes on different machines
    #couch.delete()
    couch.replicate_from(host_to_couchurl(node_address))
    return generated_blockchain



def consensus():
    """
    The consnsus algorithm.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)
    win_node = None

    for node in peers:
        response = requests.get('{}/node/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length >= current_len and Blockchain.check_chain_validity(chain):
            current_r = Blockchain.fetch_block(longest_chain[-1]).reward
            new_r = Blockchain.fetch_block(chain[-1]).reward
            if new_r > current_r:
                current_len = length
                longest_chain = chain
                win_node = node

    if longest_chain:
        blockchain = longest_chain
        couch.delete()
        couch.replicate_from(host_to_couchurl(win_node))
        return True

    return False


def announce_new_block(block_hash, block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = "{}/node/add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        data = {'hash': block_hash,
                'block': block.__dict__}
        requests.post(url,
                      data=json.dumps(data, sort_keys=True),
                      headers=headers)


def host_to_couchurl(host):
    ip = host.split('/')[2].split(':')[0]
    url = "http://admin:admin@" + ip + ":5984/"
    return url
