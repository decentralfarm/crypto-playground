import json
from web3 import Web3
import config
import time

headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))
with open("../common/axie_abi.json") as f:
    restake_abi = json.load(f)
axie_token_addr = Web3.toChecksumAddress(
    "0x32950db2a7164ae833121501c797d79e7b79d74c")
weth_token_addr = Web3.toChecksumAddress(
    "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5")
contract = web3.eth.contract(address=axie_token_addr, abi=restake_abi)

_from =Web3.toChecksumAddress(config.STAKE_ACCOUNT_ADDRESS.replace("ronin:", "0x"))
balance = contract.functions.balanceOf(_from).call()

with open("../common/axie_market_abi.json") as f:
    market_abi = json.load(f)
market_contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x213073989821f738a7ba3520c3d31a1f9ad31bbd"), abi=market_abi)

the_lapse = 2*86400     #two days
start_p = web3.toWei('0.007', 'ether')
end_p = web3.toWei('0.005', 'ether')
for i in range(balance):
    while True:
        try:
            axieId = contract.functions.tokenOfOwnerByIndex(_from,i).call()
            print(axieId)
            time.sleep(1)
            break
        except Exception:
            continue

    nonce = web3.eth.get_transaction_count(_from)

    transfer_txn = market_contract.functions.createAuction([1],
    [axie_token_addr],
    [axieId],
    [start_p],
    [end_p], 
    [weth_token_addr],
    [the_lapse]).buildTransaction({
        'chainId': 2020,
        'gas': 371098,
        'gasPrice': web3.toWei('1', 'gwei'),
        'nonce': nonce,})
        
    signed_txn = web3.eth.account.sign_transaction(transfer_txn, 
        private_key = bytearray.fromhex(config.STAKE_PK.replace("0x", "")))
    rawTxn = signed_txn.rawTransaction
    tx_hash=web3.eth.send_raw_transaction(rawTxn)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
    time.sleep(1)
