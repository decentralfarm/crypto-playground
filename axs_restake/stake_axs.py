import logging
import json
from web3 import Web3
import config
import time

headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }
web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', 
    request_kwargs={ "headers": headers }))
with open("axs_staking_abi.json") as f:
    restake_abi = json.load(f)
contract = web3.eth.contract(address=Web3.toChecksumAddress(
    "0x05b0bb3c1c320b280501b86706c3551995bc8571"), abi=restake_abi)

def parseRoninAddress(address):
  assert(address.startswith('ronin:'))
  return Web3.toChecksumAddress(address.replace('ronin:', "0x"))

def get_transaction_receipt(tx_hash):
    # Get transaction receipt
    try:
        return web3.eth.get_transaction_receipt(tx_hash)
    except:     #web3.exception.TransactionNotFound:
        print(f"Transaction {tx_hash} not found.")
        return None

def wait_for_transaction_receipt(tx_hash, timeout):
    try:
        return web3.eth.wait_for_transaction_receipt(tx_hash, timeout)
    except: #web3.exceptions.TimeExhausted
        print(f"Time Exhausted while waiting for Transaction {tx_hash}.")
        return None

def main():
    logging.basicConfig(filename=config.STAKING_LOGS, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    account_address = parseRoninAddress(config.STAKE_ACCOUNT_ADDRESS)
    nonce = web3.eth.get_transaction_count(account_address)
    print(f'Nonce: {nonce}')
    logging.info("├─Restaking...")
    transfer_txn = contract.functions.restakeRewards().buildTransaction({
    'chainId': 2020,
    'gas': 371098,
    'gasPrice': web3.toWei('1', 'gwei'),
    'nonce': nonce,})
    signed_txn = web3.eth.account.sign_transaction(transfer_txn, 
        private_key = bytearray.fromhex(config.STAKE_PK.replace("0x", "")))
    rawTxn = signed_txn.rawTransaction
    web3.eth.send_raw_transaction(rawTxn)
    tx_hash = web3.toHex(web3.keccak(rawTxn))
    logging.info(f"│  Hash: {tx_hash} - Explorer: https://explorer.roninchain.com/tx/{str(tx_hash)}")

    final_receipt = None
    tx_status = 0
    t=5
    receipt = wait_for_transaction_receipt(tx_hash, t*60)
    output = 1
    if receipt!=None:
        logging.info("│  Sleep for 60 seconds")
        time.sleep(60)
        final_receipt = get_transaction_receipt(tx_hash)
        if final_receipt != None:
                tx_status = int(final_receipt.get('status', 0)) 
                if tx_status == 1:
                    print("restake tx status Ok")
                    logging.info("├─DONE")
                    output = 0
                else:
                    print("restake tx status Not Ok")
                    logging.error("├─DONE & FAILED")
        else:
            print("restake receipt is None")
        logging.info(f"│ {final_receipt}")
    return output

if __name__ == "__main__":
    main()


