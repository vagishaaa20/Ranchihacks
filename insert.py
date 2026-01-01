import os
import json
import hashlib
from datetime import datetime
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


def insert(case_id, evidence_id, video_path):

    if not os.path.exists(video_path):
        raise Exception("Video file not found")

    # 1️⃣ Generate hash
    video_hash = generate_video_hash(video_path)
    local_timestamp = datetime.utcnow().isoformat() + "Z"

    print("========== EVIDENCE INGESTION ==========")
    print("📁 Case ID        :", case_id)
    print("🆔 Evidence ID    :", evidence_id)
    print("📄 File Path      :", video_path)
    print("🔐 SHA-256 Hash   :", video_hash)
    print("⏱ Local Time     :", local_timestamp)
    print("----------------------------------------")

    # 2️⃣ Connect to Ethereum
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not web3.is_connected():
        raise Exception("❌ Blockchain not connected")

    account = web3.eth.accounts[0]
    web3.eth.default_account = account

    print("🔗 Blockchain     : Connected")
    print("👤 Sender Account :", account)

    # 3️⃣ Load ABI
    with open(ABI_PATH) as f:
        abi = json.load(f)["abi"]

    contract = web3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    # 4️⃣ Call smart contract
    tx_hash = contract.functions.addEvidence(
        case_id,
        evidence_id,
        video_hash
    ).transact()

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    block = web3.eth.get_block(receipt.blockNumber)

    print("----------------------------------------")
    print("⛓ Blockchain Write Successful")
    print("📦 Block Number  :", receipt.blockNumber)
    print("🧾 Tx Hash       :", receipt.transactionHash.hex())
    print("⛽ Gas Used      :", receipt.gasUsed)
    print("⏱ Block Time    :", datetime.utcfromtimestamp(block.timestamp).isoformat() + "Z")
    print("========================================")

    # 5️⃣ Return structured result (for backend / frontend)
    return {
        "case_id": case_id,
        "evidence_id": evidence_id,
        "video_hash": video_hash,
        "local_timestamp": local_timestamp,
        "block_number": receipt.blockNumber,
        "block_timestamp": datetime.fromtimestamp(block.timestamp).isoformat() + "Z",
        "transaction_hash": receipt.transactionHash.hex(),
        "gas_used": receipt.gasUsed
    }


# -------- CLI SUPPORT (IMPORTANT) --------
if __name__ == "__main__":
    import sys
    insert(sys.argv[1], sys.argv[2], sys.argv[3])
