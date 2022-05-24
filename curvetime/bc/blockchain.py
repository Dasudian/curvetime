from hashlib import sha256
from uuid import getnode
import json
import time
from curvetime.db import couch

class Block:
    def __init__(self, index, timestamp, previous_hash, transactions=[], action=None, state=None, reward=None):
        """
        The init function for a block
        index: the index of the block in the chain
        transactions: data/events that need to be stored onto the blockchain
        timestame:  the time (milliseconds) when the block is created
        previous_hash: the hash value of the previous block
        action:  the action that the AI agent chose at last time step,
        state: the state of evnironment enter after action
        reward: the reward that AI agent gets from action
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.state = state
        self.action = action
        self.reward = reward


    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)


class Blockchain:
    def __init__(self, agent):
        self.unconfirmed_transactions = []
        self.agent = agent
        couch.init_db()
        self.miner = self.miner_address()
        self.chain = couch.keys()
        if not self.chain:
            self.chain = []
            self.create_genesis_block()


    def miner_address(self):
        mac = str(getnode())
        return sha256(mac.encode()).hexdigest()


    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        timestamp = time.time()
        a, s, r = self.agent.step()
        genesis_block = Block(0, timestamp, "0", [], a, s, r)
        genesis_block_hash = genesis_block.compute_hash()
        Blockchain.store_block(genesis_block_hash, genesis_block)
        self.chain.append(genesis_block_hash)


    @staticmethod
    def store_block(block_hash, block):
        couch.put(block_hash, block.__dict__)


    @staticmethod
    def fetch_block(hash):
        block = couch.get(hash)
        #if just return transactions
        return Block(**block).transactions
        #if return the whole block
        #return Block(**block)


    @property
    def last_block_hash(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block_hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        self.chain.append(proof)
        Blockchain.store_block(proof, block)
        return True

    def proof_of_work(self, block):
        """
        Function that chooses an action from the last state
        and transforms to a new state.
        """
        previous_hash = self.last_block_hash
        last_block = Blockchain.fetch_block(previous_hash)
        state = last_block.state
        a, s, r = self.agent.step(state)
        block.state = s
        block.action = a
        block.reward = r
        block.transactions.append({"transaction": "mine",
                                    "address": self.miner,
                                    "reward": r})

        computed_hash = block.compute_hash()

        return computed_hash, block

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block.state is not None and
               block.action is not None and
               block.reward is not None and
               block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block_hash in chain:
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            block = Blockchain.fetch_block(block_hash)

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            previous_hash = block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block_hash = self.last_block_hash
        last_block = Blockchain.fetch_block(last_block_hash)

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block_hash)

        proof, new_block = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        return True


    def copy_to(self):
        blocks = []
        for hash in self.chain:
            blocks.append(Blockchain.fetch_block(hash))

        return self.chain, blocks



    def copy_from(self, hash_list, block_list):
        self.chain = hash_list
        for i in range(len(hash_list)):
            Blockchain.store_block(hash_list[i], block_list[i])
