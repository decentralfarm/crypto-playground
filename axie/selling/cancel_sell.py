import json
from web3 import Web3
import config
import time

headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }

web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))

with open("../common/axie_market_abi.json") as f:
    market_abi = json.load(f)
market_contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x213073989821f738a7ba3520c3d31a1f9ad31bbd"), abi=market_abi)

_from =Web3.toChecksumAddress(config.STAKE_ACCOUNT_ADDRESS.replace("ronin:", "0x"))

done_list=[]
with open("cancel_sell.txt") as axie_lst:

    for i in axie_lst:

        if i in done_list:
            print(f"Excluding {i}")
            continue
        print(f"Last index: {i}")
        nonce = web3.eth.get_transaction_count(_from)

        transfer_txn = market_contract.functions.cancelAuction(int(i)).buildTransaction({
            'chainId': 2020,
            'gas': 371098,
            'gasPrice': web3.toWei('1', 'gwei'),
            'nonce': nonce,})
            
        signed_txn = web3.eth.account.sign_transaction(transfer_txn, 
            private_key = bytearray.fromhex(config.STAKE_PK.replace("0x", "")))
        rawTxn = signed_txn.rawTransaction
        tx_hash=web3.eth.send_raw_transaction(rawTxn)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        processed_receipt = market_contract.events.AuctionCancelled().processReceipt(tx_receipt)
        print(processed_receipt)
        print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
        time.sleep(1)
