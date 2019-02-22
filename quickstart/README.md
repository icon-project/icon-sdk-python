---

title: "ICON SDK Quickstart for Python"
excerpt: ""

---

ICON SDK Quickstart for Python is an example project for a user to use ICON SDK for Python easily with examples.

Get different types of examples as follows.

| Example       | Description |
| ------------- | ----------- |
| [WalletExample](#walletexample) | An example of creating and loading a keywallet. |
| [IcxTransactionExample](#icxtransactionexample) | An example of transferring ICX and confirming the result. |
| [TokenTransactionExample](#tokentransactionexample) | An example of transferring IRC token and confirming the result. |
| [DeployTokenExample](#deploytokenexample) | An example of deploying token. |
| [SyncBlockExample](#syncblockexample) | An example of checking block confirmation and printing the ICX and token transfer information. |

## WalletExample

This example shows how to create a new `KeyWallet` and load wallet with privateKey or Keystore file.

### Create

Create new EOA by calling `create` function. After creation, the address and private Key can be looked up.

```python
# Generates a wallet 
wallet = KeyWallet.create() 
print("address: ", wallet.get_address()) # Returns an address
print("private key: ", wallet.get_private_key()) # Returns a private key

# Output
address:  hx684c9791784c10c419eaf9322ef42792e4979712
private key:  39765c71ed1884ce08010900ed817119f4227a8b3ee7a36c906c0ae9b5b11cae
```

### Load

You can load an existing EOA by calling `load` function.

After creation, the address and private Key can be looked up.

```python
# Loads a wallet from a key store file
wallet = KeyWallet.load(TEST_PRIVATE_KEY) # bytes of the private key
print("address: ", wallet.get_address()) # Returns an address
print("private key: ", wallet.get_private_key()) # Returns a private key
```

### Store

After `KeyWallet` object creation, Keystore file can be stored by calling `store` function.

After calling `store`, Keystore file name can be looked up with the returned value.

```python
# Stores a key store file on the file path
file_path = "./test/test_keystore"
wallet.store(file_path, "abcd1234*")
```

## IcxTransactionExample

This example shows how to transfer ICX and check the result.

*For the KeyWallet and IconService creation, please refer to the information above.* 

### ICX Transfer

In this example, you can create sending KeyWallet with `TEST_PRIVATE_KEY` and receiving Keywallet. And transfer 1 ICX from `wallet1` to `wallet2`.

```python
# Wallet for sending ICX
wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)
# Wallet for receiving ICX
wallet2 = KeyWallet.create()
print("address: ", wallet2.get_address()) # Returns an address
print("private key: ", wallet2.get_private_key()) # Returns a private key
```

You can get a default step cost used to transfer ICX as follows.

```python
# Returns a step cost  
# GOVERNANCE_ADDRESS : cx0000000000000000000000000000000000000001
def get_default_step_cost():
    _call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getStepCosts")\
        .build()
    _result = icon_service.call(_call)
    default_step_cost = convert_hex_str_to_int(_result["default"])
    return default_step_cost
```

Generate transaction instance with the values as below.

```python
# Enters transaction information
transaction = TransactionBuilder()\
    .from_(wallet1.get_address())\
    .to(wallet2.get_address())\
    .value(10000)\
    .step_limit(get_default_step_cost()) \
    .nid(3) \
    .nonce(2) \
    .version(3) \
    .timestamp(int(time() * 10 ** 6))\
    .build()
```

- `nid` is networkId; 1: mainnet, 2-: etc. 

- `step_limit` is recommended by using 'default' step cost in the response of getStepCosts API.

- `timestamp` is used to prevent the identical transactions. Only current time is required (Standard unit : us). If the timestamp is considerably different from the current time, the transaction will be rejected.

Generate SignedTransaction to add signature of the transaction. 

```python
# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet1)

# Reads params to transfer to nodes
print(signed_transaction.signed_transaction_dict)
```

After calling the method of `send_transaction ` of `IconService`, you can send transaction and check the transaction’s hash value. Finally, ICX transfer is sent.

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
# Prints transaction hash
print("txHash: ", tx_hash)

# Output
txHash:  0x243438ff59561f403bac4e7b193c00d803c3aabf79249e0246451b0db7751a59
```

### Checking the Transaction Result

After transaction is sent, the result can be looked up with the returned hash value.

In this example, you can check your transaction result in every 2 seconds because of the block confirmation time.
Checking the result is as follows:

```python
# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result(tx_hash)
print("transaction status(1:success, 0:failure): ", tx_result["status"])

# Output
transaction status(1:success, 0:failure):  1
```

You can check the following information using the TransactionResult.

- status : 1 (success), 0 (failure)
- to : transaction’s receiving address
- failure : Only exists if status is 0(failure). code(str), message(str) property included
- txHash : transaction hash
- txIndex : transaction index in a block
- blockHeight : Block height of the transaction
- blockHash : Block hash of the transaction
- cumulativeStepUsed : Accumulated amount of consumed step’s until the transaction is executed in block
- stepUsed : Consumed step amount to send the transaction
- stepPrice : Consumed step price to send the transaction
- scoreAddress : SCORE address if the transaction generated SCORE (optional)
- eventLogs :  Occurred EventLog’s list during execution of the transaction.
- logsBloom : Indexed Data’s Bloom Filter value from the occurred Eventlog’s Data

### Checking the Balance

In this example, you can check the ICX balance by looking up the transaction before and after the transaction.

ICX balance can be checked with calling the `getBalance` method of `IconService`.

```python
# Gets balance
balance = icon_service.get_balance(wallet2.get_address())
print("balance: ", balance)
    
# Output 
balance:  10000 
```

## TokenTransactionExample

This example shows how to send token and check the balance.

*For KeyWallet and IconService generation, please refer to the information above.*

### Token Transfer

You can send the token that have already generated.

You can generate KeyWallet using `TEST_PRIVATE_KEY` just like in the case of  `icx_transaction_example`, then send 1 Token to the other wallet. You need token address to send your token.

You can get the default step cost to send token as follows.

```python
# Returns a step cost  
# GOVERNANCE_ADDRESS : cx0000000000000000000000000000000000000001
def get_default_step_cost():
    _call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getStepCosts")\
        .build()
    _result = icon_service.call(_call)
    default_step_cost = convert_hex_str_to_int(_result["default"])
    return default_step_cost
```

Generate Transaction with the given parameters as below. You have to add receiving address and value by entering the given key name('_to', '_value')  to send the token. Otherwise, the transaction will be rejected.

- `nid` is networkId; 1: mainnet, 2-: etc. 

- `step_limit` is recommended by using 'default' step cost multiplied by 2 in the response of getStepCosts API.

- `timestamp` is used to prevent the identical transactions. Only current time is required (Standard unit : us). If the timestamp is considerably different from the current time, the transaction will be rejected.

- `method` is 'transfer' in this case.

- `params` You must enter the given key name('\_to', '\_value'). Otherwise, the transaction will be rejected.

```python
# You must enter the given key name("_to", "_value"). Otherwise, the transaction will be rejected.
params = {"_to": wallet2.get_address(), "_value": 10}

# Enters transaction information.
call_transaction = CallTransactionBuilder()\
    .from_(wallet1.get_address())\
    .to(SCORE_ADDRESS) \
    .step_limit(get_default_step_cost()*2)\
    .nid(3) \
    .nonce(4) \
    .method("transfer")\
    .params(params)\
    .build()
```

Generate `SignedTransaction` to add signature to your transaction.

```python
# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(call_transaction, wallet1)

# Reads params to transfer to nodes
print(signed_transaction.signed_transaction_dict)
```

 Call `sendTransaction` of `IconService` to check the transaction hash. Token transaction is sent.

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)

# Prints transaction hash
print("txHash: ", tx_hash)

# Output
txHash: 0x6b17886de346655d96373f2e0de494cb8d7f36ce9086cb15a57d3dcf24523c8f
```

### Checking the Transaction Result

You can check the result with the returned hash value of the transaction.

In this example, you can check your transaction result in every 2 seconds because of the block confirmation time. Checking the result is as follows:

```python
# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result(tx_hash)
print("transaction status(1:success, 0:failure): ", tx_result["status"])

# Output
transaction status(1:success, 0:failure):  1
```

*For the TransactionResult, please refer to the `icx_transaction_example`.*

### Checking the Token Balance

In this example, you can check the token balance before and after the transaction.

You can check the token balance by calling `balanceOf` from the token SCORE.

- `method` is 'balanceOf' in this case 

- `params` should be put with '_owner' data. Otherwise, your transaction will be rejected.

```python
params = {
    "_owner": wallet2.get_address()
}

call = CallBuilder()\
    .from_(wallet1.get_address())\
    .to(SCORE_ADDRESS)\
    .method("balanceOf")\
    .params(params)\
    .build()

result = icon_service.call(call)
print("balance: ", convert_hex_str_to_int(result))

# Output
balance:  1000000000000000000000
```

## DeployTokenExample

This example shows how to deploy token and check the result.

*For the KeyWallet and IconService generation, please refer to the information above.*

### Token Deploy

You need the SCORE Project to deploy token.

In this example, you will use `standard_token.zip` from the `sample_data` folder.

- standard_token.zip : TokenStandard SCORE Project Zip file.

 Generate Keywallet using `TEST_PRIVATE_KEY`, then read the binary data from `standard_token.zip` by using the function `gen_deploy_data_content`.

- score_path: File path where the zip file of SCORE is on.

```python
# Reads the zip file 'standard_token.zip' and returns bytes of the file
install_content_bytes = gen_deploy_data_content(score_path)

# Loads a wallet from a key store file
wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)
```

You can get max step limit to send token as follows.

```python
# Returns a max step limit
# GOVERNANCE_ADDRESS : cx0000000000000000000000000000000000000001
def get_max_step_limit():
    _param = {
        "context_type": "invoke"
    }
    _call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getMaxStepLimit")\
        .params(_param)\
        .build()
    _result = icon_service.call(_call)
    return convert_hex_str_to_int(_result)
```

Generate transaction with the given values.

- `SCORE_INSTALL_ADDRESS` uses cx0 to deploy SCORE.

- `step_limit` is put by max step limit for sending transaction.

- `params` enters the basic information of the token you want to deploy. It must enter the given values, 'initialSupply' data. Otherwise, your transaction will be rejected. 

```python
params = {
    "initialSupply": 2000
}
    
# Enter transaction information.
deploy_transaction = DeployTransactionBuilder()\
        .from_(wallet1.get_address())\
        .to(SCORE_INSTALL_ADDRESS) \
        .step_limit(get_max_step_limit())\
        .nid(3)\
        .nonce(3)\
        .content_type("application/zip")\
        .content(install_content_bytes)\
        .params(params)\
        .version(3)\
        .build()
```

Generate SignedTransaction to add signature to the transaction. You can check the transaction hash value by calling sendTransaction from `IconService` Token transfer is now completed.

```python
# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet1)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)

# Prints transaction hash
print("txHash: ", tx_hash)
```

### Checking the Transaction Result

After sending the transaction, you can check the result with the returned hash value.

In this example, you can check your transaction result in every 2 seconds because of the block confirmation time.

If the transaction succeeds, you can check scoreAddress from the result.

You can use SCORE after SCORE audit is successfully accepted.

```python
# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result(tx_hash)
print("transaction status(1:success, 0:failure): ", tx_result["status"])
print("score address: ", tx_result["scoreAddress"])
print("waiting a second for accepting score...\n")

# Output
transaction status(1:success, 0:failure):  1
score address:  cx8c5ea60f73aafe10f9debfe2e3140b56335f5cfc
waiting a second for accepting score...
```

*For the 'TransactionResult', please refer to the `icx_transaction_example`.*

## SyncBlockExample

This example shows how to read block information and print the transaction result for every block creation.

*Please refer to above for KeyWallet and IconService creation.*

### Reading the Block Information

In this example, 'getLastBlock' is called periodically in order to check the new blocks, by updating the transaction information for every block creation.

```python
# Checks the last block height
pre_last_height = icon_service.get_block("latest")["height"]
print(f"Starts to scan forward block at block height({pre_last_height})")

# Returns the last block
last_block = icon_service.get_block("latest")

# Returns the transaction list.
tx_list = last_block["confirmed_transaction_list"]
    
# Output
Starts to scan forward block at block height(129)
```

If a new block has been created, get the transaction list. You can check the following information.

- version : json rpc server version
- to : Receiving address of transaction
- value: The amount of ICX coins to transfer to the address. If omitted, the value is assumed to be 0
- timestamp: timestamp of the transmitting transaction (unit: microseconds)
- nid : network ID (1: mainnet, 2-: etc)
- signature: digital signature data of the transaction
- txHash : transaction hash
- dataType: A value indicating the type of the data item (call, deploy, message)
- data: Various types of data are included according to dataType.

### Transaction Output

After reading the transaction result, you can check history having sent ICX or tokens. Transaction output is as follows:

```python
# Returns confirmed transaction list
tx_list = block["confirmed_transaction_list"]

if len(tx_list) > 0:
    for tx in tx_list:
        print("\ntxHash:", tx["txHash"])
        tx_result = icon_service.get_transaction_result(tx["txHash"])

        # Finds ICX transaction
        if "value" in tx and tx["value"] > 0:
            print("[ICX]")
            print("status: ", tx_result["status"])
            print("from  : ", tx["from"])
            print("to    : ", tx["to"])
            print("amount: ", tx["value"])

        # Finds token transfer
        if "dataType" in tx and tx["dataType"] == "call" and \
        "method" in tx["data"] and tx["data"]["method"] == "transfer":
            score_address = tx["to"]
            print(f"[{get_token_name(score_address)} Token({get_token_symbol(score_address)})]")
            print("status: ", tx_result["status"])
            print("from  : ", tx["from"])
            print("to    : ", tx["data"]["params"]["_to"])
            print("amount: ", convert_hex_str_to_int(tx["data"]["params"]["_value"]))

```

### Checking the Token Name & Symbol

You can check the token SCORE by calling the `name` and` symbol` functions.

```python
# Returns token name
def get_token_name(token_address: str):
    call = CallBuilder()\
        .from_(wallet.get_address())\
        .to(token_address)\
        .method("name")\
        .build()
    return icon_service.call(call)

# Returns token symbol
def get_token_symbol(token_address: str):
    call = CallBuilder()\
        .from_(wallet.get_address())\
        .to(token_address)\
        .method("symbol")\
        .build()
    return icon_service.call(call)
```

## References

- [ICON JSON-RPC API v3](https://icondev.readme.io/docs/json-rpc-specification) 
- [IRC2 Specification](https://github.com/icon-project/IIPs/blob/master/IIPS/iip-2.md)