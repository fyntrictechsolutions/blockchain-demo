import hashlib
import os
import uuid
try:
    from web3 import Web3
except ImportError:
    Web3 = None


def hash_file(uploaded_file):
    sha256 = hashlib.sha256()
    uploaded_file.seek(0)
    for chunk in uploaded_file.chunks():
        sha256.update(chunk)
    uploaded_file.seek(0)
    return "0x" + sha256.hexdigest()


def register_batch_on_chain(batch_code: str, doc_hash: str) -> str:
    rpc_url = os.getenv("SEPOLIA_RPC_URL")
    private_key = os.getenv("PLATFORM_WALLET_PRIVATE_KEY")
    contract_address = os.getenv("CONTRACT_ADDRESS")

    if rpc_url and private_key and contract_address:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = w3.eth.account.from_key(private_key)
        # Live smart contract call will be placed here once ABI is added
        pass

    mock_tx_hash = "0x" + uuid.uuid4().hex + uuid.uuid4().hex
    print(f"[BLOCKCHAIN DEV] Registered batch '{batch_code}' with doc_hash '{doc_hash}'")
    print(f"[BLOCKCHAIN DEV] Generated Transaction Hash: {mock_tx_hash}")
    return mock_tx_hash