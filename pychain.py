# Initial imports
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import streamlit as st
import pandas as pd
import hashlib


# Create a Record Data Class
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float


# Create a Block Data Class for storing user data and hash it
@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


# Create PyChain Data Class to help with proof of work, adding blocks, and validation
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True


# Add cache decorator for Streamlit and define setup function to initialize the blockchain
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

# Use markdown to decorate app
st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

# Run the setup function and save it as pychain
pychain = setup()


# Intake sender data from receiver
sender = st.text_input("Sender")

# Intake receiver data from user
receiver = st.text_input("Receiver")

# Intake amount data from user
amount = st.text_input("Amount")


# Add a button to create new blocks using record data, creator_id data and the previous block's hash
if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()
    new_block = Block(
        record=Record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    # Add the new block to the chain and celebrate with soem balloons
    pychain.add_block(new_block)
    st.balloons()


# Use markdown to decorate app
st.markdown("## The PyChain Ledger")

# Create a dataframe using pychain data and display it
pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Create difficulty slider for sidebar
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

# Create block inspector for sidebar and display the selected block
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

# Add a button to display whether or not the chain is valid
if st.button("Validate Chain"):
    st.write(pychain.is_valid())