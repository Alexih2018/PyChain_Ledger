################################################################################
# Imports

import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

################################################################################
# Step 1:

# Defining a new Python data class named `Record` with a
# formalized data structure that consists of the `sender`, `receiver`, and
# `amount` attributes.

@dataclass
class Record:
    sender: str
    receiver: str
    amount: float
    
# Step 2:

# 1. Add the `record` attribute to the Block class.
# 2. Set the data type of the `record` attribute to `Record`.


@dataclass
class Block:

    record: Record
    creator_id: int
    prev_hash: str = 0
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: str = 0

    # Adding a new function called `hash_block`
    def hash_block(self):
        
        # Adding an instance of the `sha256` hashing function
        sha = hashlib.sha256()
        
        # Encoding the Block's data attribute
        record = str(self.record).encode()
        # Updating the encoded data using the hashing function
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        # Return the hashes of all the Block class attributes
        return sha.hexdigest()

# Adding a `difficulty` data attribute to the `PyChain` data class
# with a data type of `int` and a default value of 4.

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()
    
        # Adding a `num_of_zeros` data attribute that multiplies the string value ("0") by the `difficulty` value.

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Winning Hash", calculated_hash)
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

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit

@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", '0')])

pychain = setup()

st.markdown("# PyChain: A Python Blockchain Application")
st.markdown("## Store Data in the Chain")

################################################################################

# Step 3:

# Adding a text input area to get a value for `sender` from the user.

sender_data = st.text_input("Sender Data")

# Adding a text input area wto get a value for `receiver` from the user.

receiver_data = st.text_input("Receiver Data")

# Adding a number input area to get a value for `amount` from the user.

amount_data = st.number_input("Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    new_block = Block(
        record=Record(sender_data, receiver_data, amount_data),
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code

st.markdown("## The PyChain Ledger")

# Creating a Pandas DataFrame to display the `PyChain` ledger

pychain_df = pd.DataFrame(pychain.chain)

# There is a bug in Arrow which causes a conversion to pyarrow.DataType to fail. Thus, an error is thrown when trying to display df.dtypes.
# The current workaround is to convert all cells to strings with df.dtypes.astype(str) until the issue is resolved

pychain_df_str = pychain_df.dtypes.astype(str)

# Using the Streamlit `write` function to display the `PyChain` DataFrame

st.write(pychain_df_str)

# Adding a Streamlit slider named "Block Difficulty" that allows the user to update a difficulty value, setting it equal to the variable `difficulty`

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)

# Updating the `difficulty` data attribute of the `PyChain` data class (`pychain.difficulty`) with this new `difficulty` value that is selected by the user

pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())

################################################################################
