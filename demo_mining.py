#!/usr/bin/env python3
"""
demo_mining.py

A simplified demonstration of mining a block and then verifying it
among 'other nodes' in a toy blockchain context.
"""

import time
import hashlib


class Block:
    """
    A simplified block structure.

    Attributes:
        index       (int)   : The block's position in the chain.
        timestamp   (float) : The time the block was created.
        data        (str)   : Arbitrary block data (like transactions).
        prev_hash   (str)   : The hash of the previous block in the chain.
        nonce       (int)   : Incremented during mining to find a valid hash.
        hash        (str)   : The final hash of this block once mined.
        difficulty  (int)   : Number of leading zeros required for a valid hash.
    """

    def __init__(self, index, data, prev_hash='', difficulty=4):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = None

    def compute_hash(self):
        """
        Produces a SHA-256 hash of the block’s critical fields.
        """
        block_string = (
                str(self.index) +
                str(self.timestamp) +
                str(self.data) +
                str(self.prev_hash) +
                str(self.nonce)
        )
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self):
        """
        Repeatedly increments nonce until the block's hash meets the difficulty target.
        """
        print(f"Mining block #{self.index} ...")
        target_prefix = '0' * self.difficulty  # e.g. '0000' for difficulty=4

        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(target_prefix):
                print(f"Block #{self.index} mined! Nonce: {self.nonce} | Hash: {self.hash}")
                break
            else:
                self.nonce += 1


class Blockchain:
    """
    A simple blockchain structure. Holds a list of blocks.
    """

    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        # Create the 'genesis' block
        self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        """
        Creates the first block in the chain with a preset index and 'prev_hash' of '0'.
        """
        genesis_block = Block(index=0, data="Genesis Block", prev_hash='0', difficulty=self.difficulty)
        genesis_block.mine_block()  # Typically you might set a pre-known genesis, but here we 'mine' it.
        return genesis_block

    def get_latest_block(self):
        """
        Retrieves the most recent block in the chain.
        """
        return self.chain[-1]

    def add_block(self, new_block):
        """
        Mines the new block and adds it to the chain.
        """
        new_block.prev_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validates the entire chain by checking:
         1. Block hashes below the difficulty target.
         2. Linkage via prev_hash.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            # Recompute the hash for current_block
            recalculated_hash = current_block.compute_hash()
            if current_block.hash != recalculated_hash:
                print(f"Block #{current_block.index} hash mismatch!")
                return False

            # Check the block is linked correctly
            if current_block.prev_hash != prev_block.hash:
                print(f"Block #{current_block.index} prev_hash mismatch!")
                return False

            # Check the difficulty requirement
            if not current_block.hash.startswith('0' * current_block.difficulty):
                print(f"Block #{current_block.index} does not meet difficulty requirement!")
                return False

        return True


def simulate_distributed_verification(chain):
    """
    Simulate how other 'nodes' would verify the newly mined blocks.
    In reality, each node independently checks the block data, prev_hash linkage,
    and that the block hash meets the difficulty target.

    Here, we'll just demonstrate that once a block is broadcast, all nodes
    re-compute and confirm the chain's validity.
    """
    print("\n=== Simulating distributed verification ===")
    # In a real network, each node has a copy of the chain
    # They verify the chain from start to finish
    # We'll just call the is_chain_valid() method to simulate that logic

    if chain.is_chain_valid():
        print("All nodes confirm: The chain is valid!")
    else:
        print("Some node found an inconsistency: The chain is invalid!")


def main():
    # Create a new blockchain with desired difficulty
    difficulty = 5  # Lower the difficulty so it mines quickly for the demo
    my_chain = Blockchain(difficulty=difficulty)

    # Mine and add a few new blocks
    block_data_list = [
        "Transaction Data #1",
        "Transaction Data #2",
        "Transaction Data #3"
    ]

    for i, data in enumerate(block_data_list, start=1):
        print(f"\nAdding Block #{i} with data: '{data}'")
        new_block = Block(index=i, data=data, difficulty=difficulty)
        my_chain.add_block(new_block)

    # Once blocks are added, simulate how other nodes confirm the chain
    simulate_distributed_verification(my_chain)


if __name__ == "__main__":
    main()
