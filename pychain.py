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


# Create a Block Data Class for storing user data
@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    # Hash the Block data and return the hash
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


# Create PyChain Data Class 
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

################################################################################
# Step 3:
# Add Relevant User Inputs to the Streamlit Interface

# Code additional input areas for the user interface of your Streamlit
# application. Create these input areas to capture the sender, receiver, and
# amount for each transaction that you’ll store in the `Block` record.
# To do so, complete the following steps:

# 3. Add an input area where you can get a value for `receiver` from the user.
# 4. Add an input area where you can get a value for `amount` from the user.
# 5. As part of the Add Block button functionality, update `new_block` so that `Block` consists of an attribute named `record`, which is set equal to a `Record` that contains the `sender`, `receiver`, and `amount` values. The updated `Block`should also include the attributes for `creator_id` and `prev_hash`.



# Intake sender data from receiver
sender = st.text_input("Sender")

# Intake receiver data from user
receiver = st.text_input("Receiver")

# Intake amount data from user
amount = st.text_input("Amount")


if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()


    new_block = Block(
        record=Record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################

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

################################################################################
# Step 4:
# Test the PyChain Ledger by Storing Records

# Test your complete `PyChain` ledger and user interface by running your
# Streamlit application and storing some mined blocks in your `PyChain` ledger.
# Then test the blockchain validation process by using your `PyChain` ledger.
# To do so, complete the following steps:

# 1. In the terminal, navigate to the project folder where you've coded the
#  Challenge.

# 2. In the terminal, run the Streamlit application by
# using `streamlit run pychain.py`.

# 3. Enter values for the sender, receiver, and amount, and then click the "Add
# Block" button. Do this several times to store several blocks in the ledger.

# 4. Verify the block contents and hashes in the Streamlit drop-down menu.
# Take a screenshot of the Streamlit application page, which should detail a
# blockchain that consists of multiple blocks. Include the screenshot in the
# `README.md` file for your Challenge repository.

# 5. Test the blockchain validation process by using the web interface.
# Take a screenshot of the Streamlit application page, which should indicate
# the validity of the blockchain. Include the screenshot in the `README.md`
# file for your Challenge repository.
