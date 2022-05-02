import json
from web3 import Web3
import config
headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))
with open("axs_staking_abi.json") as f:
    restake_abi = json.load(f)
contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x05b0bb3c1c320b280501b86706c3551995bc8571"), abi=restake_abi)
nonce = web3.eth.get_transaction_count(Web3.toChecksumAddress(
    config.STAKE_ACCOUNT_ADDRESS.replace("ronin:", "0x")))
transfer_txn = contract.functions.restakeRewards().buildTransaction({
    'chainId': 2020,
    'gas': 371098,
    'gasPrice': web3.toWei('1', 'gwei'),
    'nonce': nonce,})
signed_txn = web3.eth.account.sign_transaction(transfer_txn, 
    private_key = bytearray.fromhex(config.STAKE_PK.replace("0x", "")))
rawTxn = signed_txn.rawTransaction
web3.eth.send_raw_transaction(rawTxn)
print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
