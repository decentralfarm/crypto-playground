import json
from web3 import Web3
import config
import random
import os
import requests
headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
# web3txn = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc',
    # request_kwargs={ "headers": headers }))
web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/', 
    request_kwargs={ "headers": headers }))

_from = Web3.toChecksumAddress(config.POLY_ACCOUNT_ADDR)
def validAddr(to):
    if to is None:
        return False
    try:
        retTo = Web3.toChecksumAddress(to)
        return True
    except:
        return False

def balance():
    return web3.eth.get_balance(_from)

def gift(DESTINATION, amount):
    _to = Web3.toChecksumAddress(DESTINATION)
    bal = balance()
    print(web3.eth.accounts)
    if bal ==0:
        print("No matic in this account")
        return 'No matic in this account'
    response = requests.get('https://gasstation-mainnet.matic.network/v2').json()
    mx_fee =response['standard']['maxFee']   
    nonce = web3.eth.get_transaction_count(_from)
    tx = {
        'nonce':nonce,
        'to': _to,
        'from': _from,
        'value': web3.toWei(amount, 'ether'),
        'gas': 21000,
        # 'maxFeePerGas': web3.toWei(mx_fee, 'gwei'),
        'gasPrice': web3.toWei(mx_fee, 'gwei'),
        'chainId': 137
    }

    # transfer_txn = contract.functions.transfer(_to, amount).buildTransaction({
    #     'chainId': 80001,
    #     'gas': 300000,
    #     'gasPrice': web3.toWei('0', 'gwei'),
    #     'nonce': nonce,})
    signed_txn = web3.eth.account.sign_transaction(tx, 
        private_key = bytearray.fromhex(config.POLY_ACCOUNT_PK.replace("0x", "")))
    rawTxn = signed_txn.rawTransaction
    tx_hash=web3.eth.send_raw_transaction(rawTxn)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Check: https://polygonscan.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
    return f'https://polygonscan.com/tx/{web3.toHex(web3.keccak(rawTxn))}'
