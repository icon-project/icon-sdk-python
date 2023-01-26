[![unittest](https://img.shields.io/github/actions/workflow/status/icon-project/icon-sdk-python/iconsdk-workflow.yml?branch=master&label=unittest&logo=github)](https://github.com/icon-project/icon-sdk-python/actions/workflows/iconsdk-workflow.yml)
[![PyPI - latest](https://img.shields.io/pypi/v/iconsdk?label=latest&logo=pypi)](https://pypi.org/project/iconsdk)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/iconsdk?logo=pypi)](https://pypi.org/project/iconsdk)

# ICON SDK for Python

ICON SDK for Python is a collection of libraries which allows you to interact with a local or remote ICON node using an HTTP connection.

This document describes how to interact with ICON Network using the ICON SDK for Python, including SDK installation, API usage guide, and code examples.

## Requirements

- Python 3.7 or later.

## Installation

Setup a virtual environment first, and install ICON SDK.

```shell
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install iconsdk
```

## Using the SDK

### Create `IconService` and Set Provider

You need to create an `IconService` instance and set a provider.

- The **IconService** class contains a set of API methods. It accepts an `HTTPProvider` which serves the purpose of connecting to HTTP and HTTPS based JSON-RPC servers.

- A **provider** defines how the `IconService` connects to ICON node.

- The **HTTPProvider** takes a base domain URL where the server can be found. For local development, this would be something like `http://localhost:9000`.

Here is an example of calling a simple API method to get a block by its height:

```python
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

# Creates an IconService instance using the HTTP provider and set a provider.
icon_service = IconService(HTTPProvider("http://localhost:9000", 3))

# Gets a block by a given block height.
block = icon_service.get_block(1209)
```

### Using Logger

Set a logger named `ICON-SDK-PYTHON` if necessary. Use `set_logger` function to set log level like "DEBUG", "INFO", etc as shown below.

```python
from iconsdk.utils import set_logger

# Sets level in the logger. In this case, the handler is default StreamHandler which writes logging records, appropriately formatted, to a stream.
set_logger("DEBUG")
```

You can also set logger with a specific handler like `FileHandler` or `SteamHandler` and user own log format as shown below.

```python 
from logging import StreamHandler, Formatter

# Sets level in the logger. In this case, the handler is FileHandler which writes formatted logging records to disk files.
handler = FileHandler("./icon-sdk-python.log", mode='a', encoding=None, delay=False)

# Sets user own log format.
formatter = Formatter('%(asctime)s %(name)-12s %(levelname)-5s %(filename)-12s %(lineno)-4s %(funcName)-12s %(message)s')

set_logger("DEBUG", handler, formatter)
```


## Queries

```python
from iconsdk.builder.call_builder import CallBuilder

# Returns block information by block height
block = icon_service.get_block(1000)

# Returns block information by block hash
block = icon_service.get_block("0x000...000")

# Returns the last block information
block = icon_service.get_block("latest")

# Returns the balance of the account of given address
balance = icon_service.get_balance("hx000...1")

# Returns a list of the SCORE APIs
score_apis = icon_service.get_score_api("cx000...1")

# Returns the total supply of ICX
total_supply = icon_service.get_total_supply()

# Returns information about a transaction requested by transaction hash
tx = icon_service.get_transaction("0x000...000")

# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000")

# Returns the data based on the hash
tx_result = icon_service.get_data_by_hash("0x000...000")

# Returns block header for specified height.
tx_result = icon_service.get_block_header_by_height(1000)

# Returns votes for the block specified by height
tx_result = icon_service.get_votes_by_height(1000)

# Returns proof for the receipt. Proof, itself, may include the receipt.
tx_result = icon_service.get_proof_for_result("0x000...000", 0)

# Returns proof for the receipt and the events in it. The proof may include the data itself.
tx_result = icon_service.get_proof_for_events("0x000...000", 0, [ "0x0", "0x2" ])

# Generates a call instance using the CallBuilder
call = CallBuilder().from_(wallet.get_address())\
                    .to("cx000...1")\
                    .method("balance_of")\
                    .params({"address": "hx000...1"})\
                    .height(100)\
                    .build()

# Executes a call method to call a read-only API method on the SCORE immediately without creating a transaction
result = icon_service.call(call)
```


### get_block

```python
get_block(value)
```

* Function A
  * Returns block information by block height
  * Delegates to **icx_getBlockByHeight** RPC method

* Function B
  * Returns block information by block hash
  * Delegates to **icx_getBlockByHash** RPC method

* Function C
  * Returns the last block information
  * Delegates to **icx_getLastBlock** RPC method

#### Parameters

* Function A
  * value : Integer of a block height
* Function B
  * value : Hash of a block prefixed with '0x'
* Function C
  * value : 'latest'

#### Returns

Block data

[Example of a returned block data](https://github.com/icon-project/icon-rpc-server/blob/master/docs/icon-json-rpc-v3.md#icx_getlastblock)

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns block information by block height
block = icon_service.get_block(1000)

# Returns block information by block hash
block = icon_service.get_block("0x000...000")

# Returns the last block information
block = icon_service.get_block("latest")
```



### get_balance

```python
get_balance(address: str, height: int = None)
```

Returns the ICX balance of the given EOA or SCORE

Delegates to **icx_getBalance** RPC method

#### Parameters

address : An address of EOA or SCORE

height(optional) : Block height

#### Returns

Number of ICX coins

#### Error Cases

* AddressException : Address is invalid.
* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns the ICX balance of the given EOA or SCORE
balance = icon_service.get_balance("hx000...1")
```



### get_score_api

```python
get_score_api(address: str, height: int = None)
```

Returns SCORE's external API list

Delegates to **icx_getScoreApi** RPC method

#### Parameters

address : A SCORE address to be examined

height(optional) : Block height

#### Returns

A list of API methods of the SCORE and its information

Fields :

* type : Method type;  function, fallback, or eventlog
* name : Function name on the SCORE
* inputs : A list of information of parameters
  * name : Parameter name
  * type : Parameter type ; int, str, bytes, bool, Address
  * indexed : In the case of eventlog, tells if the parameter is indexed.
* outputs : Return value
  * type : Return value type ; int, str, bytes, bool, Address
* Readonly : External (readonly=True)
* Payable: Payable

#### Error Cases

* AddressException : Address is invalid.
* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns SCORE's external API list
score_apis = icon_service.get_score_api("cx000...1")
```



### get_total_supply

```python
get_total_supply(height: int = None)
```

Returns total ICX coin supply that has been issued

Delegates to **icx_getTotalSupply** RPC method

#### Parameters

height(optional) : Block height

#### Returns

Total number of ICX coins issued

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns total ICX coin supply that has been issued
total_supply = icon_service.get_total_supply()
```



### get_transaction

```python
get_transaction(tx_hash: str)
```

Returns the transaction information requested by transaction hash

Delegates to **icx_getTransactionByHash** RPC method

#### Parameters

tx_hash : Transaction hash prefixed with '0x'

#### Returns

Information about a transaction

Fields :

- version : Protocol version (3 for V3)
- from : An EOA address that created the transaction
- to : An EOA address to receive coins, or SCORE address to execute the transaction
- value : Amount of ICX coins in loop to transfer. When omitted, assumes 0. (1 icx = 10 ^ 18 loop)
- stepLimit :  Maximum step allowance that can be used by the transaction
- timestamp : Transaction creation time. Timestamp is in microseconds.
- nid : Network ID (1 for Main net, etc)
- nonce : An arbitrary number used to prevent transaction hash collision
- txHash : Transaction hash
- txIndex : Transaction index in a block. Null when it is pending.
- blockHeight : Block height including the transaction. Null when it is pending
- blockHash : Block hash including the transaction. Null when it is pending.
- signature : Signature of the transaction
- dataType : Data type; call, deploy, message
- data : Contains various type of data depending on the dataType

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns the transaction information requested by transaction hash
tx = icon_service.get_transaction("0x000...000")
```



### get_transaction_result

```python
get_transaction_result(tx_hash: str)
```

Returns the transaction result requested by transaction hash

Delegates to **icx_getTransactionResult** RPC method

#### Parameters

tx_hash : Hash of a transaction prefixed with '0x'

#### Returns

A transaction result object

Field :

* status : 1 on success, 0 on failure
* to : Recipient address of the transaction
* failure : This field exists when status is 0. Contains code(str) and message(str)
* txHash : Transaction hash
* txIndex : Transaction index in the block
* blockHeight : Block height including the transaction
* blockHash : Block hash including the transaction
* cumulativeStepUsed : Sum of stepUsed by this transaction and all preceding transactions in the same block
* stepUsed : The amount of step used by this transaction
* stepPrice: The step price used by this transaction
* scoreAddress : A SCORE address if the transaction created a new SCORE. (optional)
* eventLogs : Array of eventlogs generated by this transaction
* logsBloom : Bloom filter to quickly retrieve related eventlogs

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns the transaction result requested by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000")
```


### get_data_by_hash

```python
get_data_by_hash(hash: str)
```

Get data by hash.

It can be used to retrieve data based on the hash algorithm (SHA3-256).

Following data can be retrieved by a hash.

* BlockHeader with the hash of the block
* Validators with BlockHeader.NextValidatorsHash
* Votes with BlockHeader.VotesHash
* etc…

Delegates to **icx_getDataByHash** RPC method

#### Parameters

hash : The hash value of the data to retrieve.

#### Returns

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
tx_result = icon_service.get_data_by_hash("0x000...000")
```

### get_block_header_by_height

```python
get_block_header_by_height(height: int)
```
Get block header for specified height.

Delegates to **icx_getBlockHeaderByHeight** RPC method

#### Parameters

height : The height of the block

#### Returns

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
tx_result = icon_service.get_block_header_by_height(1000)
```

### get_votes_by_height

```python
get_votes_by_height(height: int)
```
Get votes for the block specified by height.

Normally votes for the block are included in the next. So, even though the block is finalized by votes already, the block including votes may not exist. For that reason, we support this API to get votes as proof for the block.

Delegates to **icx_getVoteByHeight** RPC method

#### Parameters

height : The height of the block

#### Returns

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
tx_result = icon_service.get_vote_by_height(1000)
```


### call

```python
call(call: Call)
```

Calls SCORE's external function which is read-only without creating a transaction.

Delegates to **icx_call** RPC method

#### Parameters

Call object made by **CallBuilder**

Fields :

* from : Message sender's address (optional)
* to : A SCORE address that will handle the message
* method : name of an external function
* params : Parameters to be passed to the function (optional). A data type of params should be **dict**.


#### Returns

Values returned by the executed SCORE function

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Generates a call instance using the CallBuilder
call = CallBuilder().from_(wallet.get_address())\
                    .to("cx000...1")\
                    .method("balance_of")\
                    .params({"address": "hx000...1"})\
                    .build()

# Calls SCORE's external function which is read-only without creating a transaction
result = icon_service.call(call)
```



## KeyWallet

To send transactions, first, you should make an instance of your wallet.

You can make an instance of the wallet using bytes of the private key or from a keystore file.

```python
from iconsdk.wallet.wallet import KeyWallet

# Generates a wallet
wallet = KeyWallet.create()

# Loads a wallet from bytes of the private key
wallet = KeyWallet.load(b'-B\x99...xedy')

# Loads a wallet from a keystore file
wallet = KeyWallet.load("./keystore", "password")

# Stores a keystore file on the file path
wallet.store("./keystore", "password") # throw exception if having an error.

# Returns an Address
wallet.get_address()

# Returns a private key
wallet.get_private_key()

# Signs the transaction
signature = wallet.sign(b'D8\xe9...\xfc')
```

### create

```python
create()
```

Generates an instance of Wallet without a specific private key

#### Parameters

None

#### Returns

An instance of Wallet class

#### Example

```python
# Generates a wallet
wallet = KeyWallet.create()
```



### load

```python
load(private_key: bytes)
```

Loads a wallet from bytes of the private key and generates an instance of Wallet

#### Parameters

private_key : Bytes of the private key

#### Returns

An instance of Wallet class

#### Error Cases

* DataTypeException : Private key is invalid.

#### Example

```python
# Loads a wallet from bytes of the private key
wallet = KeyWallet.load(b'-B\x99...xedy')
```



### load

```python
load(file_path: PathLikeObject, password: str)
```
> **Note**:
> type alias `PathLikeObject` is defined in `utils/__init__.py`
> ```python
> PathLikeObject = Union[str, bytes, os.PathLike]
> ```

Loads a wallet from a keystore file with your password and generates an instance of Wallet

#### Parameters

* file_path : File path of the keystore file

* password : Password for the keystore file. Password must include alphabet character, number, and special character

#### Returns

An instance of Wallet class

#### Error Cases

* KeyStoreException: Key store file is invalid.

#### Example

```python
# Loads a wallet from a keystore file
wallet = KeyWallet.load("./keystore", "password")
```



### store

```python
store(file_path, password)
```

Stores data of an instance of a derived wallet class on the file path with your password

#### Parameters

- file_path : File path of the keystore file

- password :  Password for the keystore file. Password must include alphabet character, number, and special character

#### Returns

None

#### Error Cases

* KeyStoreException: Key store file is invalid.

#### Example

```python
# Stores a keystore file on the file path
wallet.store("./keystore", "password") # throw exception if having an error.
```



### get_address

```python
get_address()
```

Returns an EOA address

The format of your account (which is generated from your public key) is hxfd7e4560ba363f5aabd32caac7317feeee70ea57.

#### Parameters

None

#### Returns

 An EOA address

#### Example

```python
# Returns an EOA address
wallet.get_address()
```



### get_private_key

```python
get_private_key()
```

Returns hex string of the private key of the wallet

#### Parameters

None

#### Returns

Hex string of the private key

#### Example

```python
# Returns the private key
wallet.get_private_key()
```



### sign

```python
sign(data: bytes)
```

Returns bytes of the ECDSA-SHA256 signature made from the data

#### Parameters

data : bytes of the transaction

#### Returns

Bytes of the signature

#### Error Cases

* DataTypeException : Data type is invalid.

#### Example

``` python
# Signs the transaction
signature = wallet.sign(b'D8\xe9...\xfc')
```



## Transactions

### Generating a Transaction

Next, you should create an instance of the transaction using different types of **transaction builders** as follows:

### Signing a Transaction

Before sending a transaction, the transaction should be signed by using **SignedTransaction** class. The SignedTransaction class is used to sign the transaction by returning an instance of the signed transaction as demonstrated in the example below. The instance of the signed transaction has the property of a signature.

### Sending a Transaction

Finally, you can send a transaction with the signed transaction object as follows:

### Examples

```python
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder,
    DepositTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction

# Generates an instance of transaction for sending icx.
transaction = TransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(150000000)\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .build()

# Generates an instance of transaction for deploying SCORE.
transaction = DeployTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .content_type("application/zip")\
    .content(b'D8\xe9...\xfc')\
    .params(params)\
    .build()

# Generates an instance of transaction for calling method in SCORE.
transaction = CallTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .method("transfer")\
    .params(params)\
    .build()

# Generates an instance of transaction for sending a message.
transaction = MessageTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .data("0x74657374")\
    .build()
    
# Generates an instance of transaction for adding or withdrawing a deposit.
# Case0: Adding a deposit 
transaction = DepositTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(5000*(10**18))\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .action("add") \
    .build()
    
# Case1: Withdrawing the deposit
transaction = DepositTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .action("withdraw") \
    .id(tx_hash) \
    .build()

# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```



### TransactionBuilder

Builder for a **Transaction** object

#### Methods

* from_ : The wallet address making a transaction. The default address is your account address.
* to : The wallet address to receive coin or SCORE address to receive a transaction.
* value : The amount of ICX to be sent. (Optional)
* step_limit : The maximum step value for processing a transaction.
* nid : Network ID. Default nid is 1 if you didn't set the value. (1 for Main net, etc)
* nonce :  An arbitrary number used to prevent transaction hash collision. (Optional)
* version : Protocol version (3 for V3). The default version is 3 if you didn't set the value.
* timestamp : Transaction creation time. Timestamp is in microseconds. Default timestamp is set, if you didn't set the value.
* build : Returns an ICX transaction object

#### Returns

A transaction object

#### Example

```python
# Generates an instance of transaction for sending icx.
transaction = TransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(150000000)\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .build()
```



### DeployTransactionBuilder

Builder for **DeployTransaction** object

#### Methods

* from_ : The wallet address making a transaction. The default address is your account address.
* to : The wallet address to receive coin or SCORE address to receive a transaction
* step_limit : The maximum step value for processing a transaction
* nid : Network ID. Default nid is 1 if you didn't set the value. (1 for Main net, etc)
* nonce : An arbitrary number used to prevent transaction hash collision
* content_type : Content's MIME type
* content : Binary data of the SCORE
* params : Parameters passed on the SCORE methods ; on_install (), on_update (). Data type of the params should be **dict**. (optional)
* version : Protocol version (3 for V3). The default version is 3 if you didn't set the value.
* timestamp : Transaction creation time. Timestamp is in microseconds. Default timestamp is set, if you didn't set the value.
* build : Returns a deploy transaction object

#### Returns

A deploy transaction object

#### Example

```python
# Generates an instance of transaction for deploying SCORE.
transaction = DeployTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .content_type("application/zip")\
    .content(b'D8\xe9...\xfc')\
    .params(params)\
    .build()
```



### CallTransactionBuilder

Builder for **CallTransaction** object

#### Methods

- from_ : The wallet address making a transaction. The default address is your account address.
- to : The wallet address to receive coin or SCORE address to receive a transaction
- step_limit : The maximum step value for processing a transaction
- nid : Network ID. Default nid is 1 if you didn't set the value. (1 for Main net, etc)
- nonce :  An arbitrary number used to prevent transaction hash collision
- method : Methods in the SCORE
- params : Parameters passed on the SCORE methods. Data type of the params should be **dict**. (optional)
- version : Protocol version (3 for V3). The default version is 3 if you didn't set the value.
- timestamp : Transaction creation time. Timestamp is in microseconds. Default timestamp is set, if you didn't set the value.
- Build : Returns a call transaction object

#### Returns

A call transaction object

#### Example

```python
# Generates an instance of transaction for calling method in SCORE.
transaction = CallTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .method("transfer")\
    .params(params)\
    .build()
```



### MessageTransactionBuilder

Builder for **MessageTransaction** object

#### Methods

- from_ : The wallet address making a transaction. The default address is your account address.
- to : The wallet address to receive coin or SCORE address to receive a transaction
- stepLimit : The maximum step value for processing a transaction
- nid : Network ID. Default nid is 1 if you didn't set the value. (1 for Main net, etc)
- nonce :  An arbitrary number used to prevent transaction hash collision
- data : Data by the dataType. Data type of the data should be **lowercase hex string** prefixed with '0x'.
- version : Protocol version (3 for V3). The default version is 3 if you didn't set the value.
- timestamp : Transaction creation time. Timestamp is in microseconds. Default timestamp is set, if you didn't set the value.
- build : Returns a message transaction object

#### Returns

A message transaction object

#### Example

```python
# Generates an instance of transaction for sending a message.
transaction = MessageTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .data("0x74657374")\
    .build()
```



### DepositTransactionBuilder

Builder for **DepositTransaction** object

#### Methods

- from_ : The wallet address making a transaction. The default address is your account address.
- to : SCORE address to receive a transaction
- value : The amount of ICX to be deposited. It is used only for 'add' action. (Optional)
- action : "add" or "withdraw".
- id : Transaction hash prefixed with '0x'. It is used only for 'withdraw' action. (Optional)
- stepLimit : The maximum step value for processing a transaction.
- nid : Network ID. Default nid is 1 if you didn't set the value. (1 for Main net, etc)
- nonce :  An arbitrary number used to prevent transaction hash collision.
- version : Protocol version (3 for V3). The default version is 3 if you didn't set the value.
- timestamp : Transaction creation time. Timestamp is in microseconds. Default timestamp is set, if you didn't set the value.
- build : Returns a deposit transaction object.

#### Returns

A deposit transaction object  

#### Example

```python
# Generates an instance of transaction for adding or withdrawing a deposit.
# Case0: Adding a deposit 
transaction = DepositTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(5000*(10**18))\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .action("add") \
    .build()
    
# Case1: Withdrawing the deposit
transaction = DepositTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .step_limit(1000000)\
    .nid(3)\
    .nonce(100)\
    .action("withdraw") \
    .id(tx_hash) \
    .build()
```



### SignedTransaction

```python
SignedTransaction(transaction: Transaction, wallet: Wallet)
```

Returns the signed transaction object having a signature

#### Parameters

* transaction : A transaction object not having a signature field yet
* wallet : A wallet object

#### Returns

The signed transaction object having a signature field finally

#### Error Cases

* DataTypeException : Data type is invalid.

#### Example

```python
# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet)
```



### send_transaction

```python
send_transaction(signed_transaction: SignedTransaction)
```

Sends the transaction

Delegates to **icx_sendTransaction** RPC method

Need to wait for a while after sending the transaction. Because it takes time to create consensus among nodes. We recommend 0.3 seconds at least.

#### Parameters

signed_transaction : A signed transaction object

#### Returns

Transaction hash prefixed with '0x'

#### Error Cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```



## Estimating Step

It is important to set a proper `step_limit` value in your transaction to make the submitted transaction executed successfully.

`estimate_step` API provides a way to **estimate** the Step usage of a given transaction. Using the method, you can get an estimated Step usage before sending your transaction then make a `SignedTransaction` with the `step_limit` based on the estimate.

### Examples

```python
# Generates a raw transaction without the stepLimit
transaction = TransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(150000000)\
    .nid(3)\
    .nonce(100)\
    .build()

# Returns an estimated step value
estimate_step = icon_service.estimate_step(transaction)

# Adds some margin to the estimated step
estimate_step += 10000

# Returns the signed transaction object having a signature with the same raw transaction and the estimated step
signed_transaction = SignedTransaction(transaction, wallet, estimate_step)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```

Note that the estimate can be smaller or larger than the actual amount of step to be used by the transaction, so it is recommended to add some margin to the estimate when you set the `step_limit` of the `SignedTransaction`.



### estimate_step

```python
estimate_step(transaction: Transaction)
```

Returns an estimated step of how much step is necessary to allow the transaction to complete

Delegates to **debug_estimateStep** RPC method

#### Parameters

transaction : An Transaction object made by TransactionBuilder

#### Returns

Number of an estimated step

#### Error Cases

- DataTypeException : Data type is invalid.
- JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Generates a raw transaction without the stepLimit
transaction = TransactionBuilder()\
    .from_(wallet.get_address())\
    .to("cx00...02")\
    .value(150000000)\
    .nid(3)\
    .nonce(100)\
    .build()

# Returns an estimated step value
estimate_step = icon_service.estimate_step(transaction)
```

## BTP2 extension

### get_btp_network_info

```python
def get_btp_network_info(self, id: int, height: int = None) -> dict:
```

> Returns BTP Network information for specified height and ID.
>
> Delegates to btp_getNetworkInfo RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getNetworkInfo

#### Parameters
| param  | description                  |
|--------|------------------------------|
| id     | The id of the BTP network    |
| height | The height of the main block |

#### Returns
  A BTP Network information object

### get_btp_network_type_info

```python
def get_btp_network_type_info(self, id: int, height: int = None) -> dict:
```
> Returns BTP Network Type information for specified height and ID.
>
> Delegates to btp_getNetworkTypeInfo RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getNetworkTypeInfo

#### Parameters
| param  | description                    |
|--------|--------------------------------|
| id     | The id of the BTP network type |
| height | The height of the main block   |

#### Returns
  A BTP Network Type information object

### get_btp_messages
```python
def get_btp_messages(self, height: int, network_id: int) -> list:
```

> Returns BTP messages for specified height and network ID.
>
> Delegates to btp_getMessages RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getMessages

#### Parameters
| param      | description                  |
|------------|------------------------------|
| height     | The height of the main block |
| network_id | The id of the BTP network    |

#### Returns
  A BTP Messages object

### get_btp_header
```python
def get_btp_header(self, height: int, network_id: int) -> str:
```

> Returns BTP block header for specified height and network ID.
>
> Delegates to btp_getHeader RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getHeader

#### Parameters
| param      | description                  |
|------------|------------------------------|
| height     | The height of the main block |
| network_id | The id of the BTP network    |

#### Returns
  A Base64 encoded BTP block header

### get_btp_proof
```python
def get_btp_proof(self, height: int, network_id: int) -> str:
```

> Returns BTP block proof for specified height and network ID.
>
> Delegates to btp_getHeader RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getProof

#### Parameters
| param      | description                  |
|------------|------------------------------|
| height     | The height of the main block |
| network_id | The id of the BTP network    |

#### Returns
  A Base64 encoded BTP block proof

### get_btp_source_information
```python
def get_btp_source_information(self) -> dict:
```

> Returns BTP source network information.
>
> Delegates to btp_getSourceInformation RPC method.
>
> https://github.com/icon-project/goloop/blob/master/doc/btp2_extension.md#btp_getSourceInformation

#### Returns
  A BTP network information object


## References

- [Quick Start]
- [ICON JSON-RPC API v3]
- [ICON Network]

[Quick Start]: quickstart
[ICON JSON-RPC API v3]: https://docs.icon.community/icon-stack/client-apis/json-rpc-api/v3
[ICON Network]: https://docs.icon.community/icon-stack/icon-networks

## License

This project is available under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
