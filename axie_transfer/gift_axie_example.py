import json
from web3 import Web3
import config
headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
web3txn = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc',
    request_kwargs={ "headers": headers }))
web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))
with open("gift_axie.json") as f:
    restake_abi = json.load(f)
contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x32950db2a7164ae833121501c797d79e7b79d74c"), abi=restake_abi)
_to = Web3.toChecksumAddress(config.TO_ACCOUNT_ADDRESS) # To address
_from =Web3.toChecksumAddress(config.FROM_ACCOUNT_ADDRESS) # From address
nonce = web3.eth.get_transaction_count(_from)
transfer_txn = contract.functions.safeTransferFrom(_from ,_to, 1234).buildTransaction({
    'chainId': 2020,
    'gas': 300000,
    'gasPrice': web3txn.toWei('0', 'gwei'),
    'nonce': nonce,})
signed_txn = web3txn.eth.account.sign_transaction(transfer_txn, 
    private_key = bytearray.fromhex(config.FROM_PK.replace("0x", ""))) # sender's private key
rawTxn = signed_txn.rawTransaction
tx_hash=web3txn.eth.send_raw_transaction(rawTxn)
web3txn.eth.wait_for_transaction_receipt(tx_hash)
print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
