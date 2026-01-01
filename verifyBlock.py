import os
import json
import hashlib
from datetime import datetime, timezone
from web3 import Web3

GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x485265b6f6E90A0718c750ea1988866Bd357f728"
ABI_PATH = "compiled_code.json"


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

    # 1. Recalculate hash
    computed_hash = generate_video_hash(video_path)
    print("Evidence ID    :", evidence_id)
    print("File Path      :", video_path)
    print("Computed Hash  :", computed_hash)

    # 2. Connect to blockchain
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not web3.is_connected():
        raise Exception("Blockchain not connected")

    # 3. Load ABI
    with open(ABI_PATH) as f:
        abi = json.load(f)["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    contract = web3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    # 4. Fetch stored hash
    stored_hash = contract.functions.getEvidenceHash(evidence_id).call()
    print("Stored Hash    :", stored_hash)
    print("------------------------------------------")

    # 5. Compare
    if stored_hash == computed_hash:
        print("VERIFICATION RESULT : AUTHENTIC")
        print("Evidence not tampered")
        return True
    else:
        print("VERIFICATION RESULT : TAMPERED")
        print("Evidence has been modified")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python verifyBlock.py <EVIDENCE_ID> <VIDEO_PATH>")
        exit(1)

    evidence_id = sys.argv[1]
    video_path = sys.argv[2]

    verify(evidence_id, video_path)

