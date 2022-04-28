import json
from web3 import Web3
import config
import time

headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
web3txn = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc',
    request_kwargs={ "headers": headers }))
web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))
with open("axie_abi.json") as f:
    restake_abi = json.load(f)
contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x32950db2a7164ae833121501c797d79e7b79d74c"), abi=restake_abi)

web3poly = Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/', 
    request_kwargs={ "headers": headers }))
with open("polyNFTContract.json") as fpoly:
    nft_poly_abi = json.load(fpoly)
contractPoly = web3poly.eth.contract(address=Web3.toChecksumAddress(
    "0x9a897107cE02393144b69196A522D106628c8081"), abi=nft_poly_abi)

registry_amount = contractPoly.functions.registryAmount().call()
print(f'registry amount {registry_amount}')
_from = Web3.toChecksumAddress(config.STAKE_ACCOUNT_ADDRESS.replace("ronin:", "0x"))
# mycount=1
for reg_index in range(registry_amount):
    register = contractPoly.functions.nFTRegistry(reg_index).call()
    tokenId = register[0]
    real_owner = contract.functions.ownerOf(tokenId).call()
    if real_owner != _from:
        print(f"{tokenId} Not owned, owner: {real_owner}")
        continue

    print("Owned")
    _to = Web3.toChecksumAddress(register[1].replace("ronin:", "0x"))
    balance = contract.functions.balanceOf(_from).call()
    print(f"Sending {tokenId} from {_from} to {_to}, balance: {balance}")
    
    nonce = web3.eth.get_transaction_count(_from)
    transfer_txn = contract.functions.safeTransferFrom(_from ,_to, tokenId).buildTransaction({
        'chainId': 2020,
        'gas': 300000,
        'gasPrice': web3txn.toWei('0', 'gwei'),
        'nonce': nonce,})
        
    signed_txn = web3txn.eth.account.sign_transaction(transfer_txn, 
        private_key = bytearray.fromhex(config.STAKE_PK.replace("0x", "")))
    rawTxn = signed_txn.rawTransaction
    tx_hash=web3txn.eth.send_raw_transaction(rawTxn)
    web3txn.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
    time.sleep(10)    
