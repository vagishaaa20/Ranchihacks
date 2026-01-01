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


def verify(evidence_id, video_path):

    if not os.path.exists(video_path):
        raise Exception("Video file not found")

    print("========== EVIDENCE VERIFICATION ==========")

    # 1️⃣ Recalculate hash from uploaded video
    new_hash = generate_video_hash(video_path)
    verify_time = datetime.utcnow().isoformat() + "Z"

    print("🆔 Evidence ID    :", evidence_id)
    print("📄 File Path      :", video_path)
    print("🔐 Computed Hash  :", new_hash)
    print("⏱ Verification   :", verify_time)
    print("-------------------------------------------")

    # 2️⃣ Connect to blockchain
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not web3.is_connected():
        raise Exception("❌ Blockchain not connected")

    print("🔗 Blockchain     : Connected")

    # 3️⃣ Load ABI
    with open(ABI_PATH) as f:
        abi = json.load(f)["abi"]

    contract = web3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    # 4️⃣ Fetch stored hash from blockchain
    try:
        stored_hash = contract.functions.getEvidenceHash(evidence_id).call()
    except Exception:
        print("❌ Evidence not found on blockchain")
        print("===========================================")
        return False

    print("📦 Stored Hash    :", stored_hash)
    print("-------------------------------------------")

    # 5️⃣ Compare hashes
    if stored_hash == new_hash:
        print("✅ VERIFICATION RESULT : AUTHENTIC")
        print("📌 Status             : Evidence not tampered")
        print("===========================================")
        return True
    else:
        print("❌ VERIFICATION RESULT : TAMPERED")
        print("⚠️ Status              : Evidence modified")
        print("===========================================")
        return False


# -------- CLI SUPPORT (IMPORTANT) --------
if __name__ == "__main__":
    import sys

    evidence_id = sys.argv[1]
    video_path = sys.argv[2]

    result = verify(evidence_id, video_path)

    # Exit code for backend logic
    if result:
        exit(0)   # AUTHENTIC
    else:
        exit(1)   # TAMPERED
