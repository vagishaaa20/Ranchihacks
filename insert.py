import os
import hashlib
from datetime import datetime
from web3 import Web3

# ---------------- CONFIG ---------------- #

GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE"
ABI_PATH = "compiled_code.json"

# -------------------------------------- #

def generate_video_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def insert(case_id, evidence_id, video_path):

    if not os.path.exists(video_path):
        raise Exception("Video file not found")

    # 1️⃣ Generate hash
    video_hash = generate_video_hash(video_path)
    timestamp = datetime.utcnow().isoformat()

    print("📁 Case ID:", case_id)
    print("🆔 Evidence ID:", evidence_id)
    print("🔐 Video Hash:", video_hash)
    print("⏱ Timestamp:", timestamp)

    # 2️⃣ Connect to Ethereum
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not web3.is_connected():
        raise Exception("Blockchain not connected")

    account = web3.eth.accounts[0]
    web3.eth.default_account = account

    # 3️⃣ Load ABI
    import json
    with open(ABI_PATH) as f:
        abi = json.load(f)["abi"]

    contract = web3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    # 4️⃣ Call smart contract
    tx_hash = contract.functions.addEvidence(
        evidence_id,
        case_id,
        video_hash
    ).transact()

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print("✅ Evidence added to blockchain")
    print("🔗 Tx Hash:", receipt.transactionHash.hex())

    return {
        "case_id": case_id,
        "evidence_id": evidence_id,
        "hash": video_hash,
        "tx": receipt.transactionHash.hex()
    }