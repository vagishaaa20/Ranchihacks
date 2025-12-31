import os
import hashlib
from web3 import Web3

# ---------------- CONFIG ---------------- #

GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE"
ABI_PATH = "compiled_code.json"

# --------------------------------------- #

def generate_video_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify(evidence_id, video_path):

    if not os.path.exists(video_path):
        raise Exception("Video file not found")

    # 1️⃣ Recalculate hash
    new_hash = generate_video_hash(video_path)

    # 2️⃣ Connect to blockchain
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not web3.is_connected():
        raise Exception("Blockchain not connected")

    # 3️⃣ Load ABI
    import json
    with open(ABI_PATH) as f:
        abi = json.load(f)["abi"]

    contract = web3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    # 4️⃣ Call smart contract
    is_valid = contract.f_
