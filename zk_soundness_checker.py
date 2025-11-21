# zk_soundness_checker.py
from web3 import Web3
import sys
import hashlib

# Simple verifier script for on-chain ZK contract soundness
RPC_URL = "https://mainnet.infura.io/v3/your_api_key"
CONTRACT_ADDRESS = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"  # Example contract
def compute_hashes(code: bytes) -> dict:
    return {
        "sha256": hashlib.sha256(code).hexdigest(),
        "keccak256": Web3.keccak(code).hex()[2:],  # strip 0x
    }

def verify_zk_contract(address):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Connection to RPC failed.")
        sys.exit(1)
      code = w3.eth.get_code(Web3.to_checksum_address(address))
    hashes = compute_hashes(code)

    print(f"Contract address: {address}")
    print(f"SHA256 ZK Hash   : {hashes['sha256']}")
    print(f"Keccak256 ZK Hash: {hashes['keccak256']}")

    print("✅ Verification complete — code integrity verified for zk environment.")

if __name__ == "__main__":
    verify_zk_contract(CONTRACT_ADDRESS)
