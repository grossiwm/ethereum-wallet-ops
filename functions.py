from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware

def send_ether(ganache_url, private_key, to_address, amount):
    # Connect to Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Add necessary middleware for Ganache
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Check if the connection was successful
    if not web3.is_connected():
        raise Exception("Failed to connect to Ganache.")

    # Set up the sender account from the private key
    account = Account.from_key(private_key)

    # Set up the transaction details
    tx_details = {
        'to': to_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
    }

    # Sign the transaction
    signed_tx = account.sign_transaction(tx_details)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()

def get_balance(ganache_url, address):
    # Conectar ao Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Verificar se a conexão foi bem sucedida
    if not web3.is_connected():
        raise Exception("Failed to connect to Ganache.")

    # Obter o saldo do endereço em Wei
    balance_wei = web3.eth.get_balance(address)

    # Converter o saldo para Ether
    balance_ether = web3.from_wei(balance_wei, 'ether')

    return balance_ether

'''
ganache_url = 'http://localhost:8545'
private_key = 'your_private_key_here'
to_address = 'destination_address_here'
amount = 1  # Send 1 Ether

tx_hash = send_ether(ganache_url, private_key, to_address, amount)
print(f'Transaction successfully sent! Transaction hash: {tx_hash}')
'''