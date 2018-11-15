



# ICON SDK for Python

ICON SDK for Python is a collection of libraries which allow you to interact with a local or remote Loopchain node, using an HTTP connection. The following documentation will guide you through installing and running ICON SDK for Python as well as providing an API reference documentation examples. It is reference to [ICON JSON-RPC API **v3**](https://github.com/icon-project/icon-rpc-server/blob/master/docs/icon-json-rpc-v3.md).



<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [ICON SDK for Python](#icon-sdk-for-python)
  - [Quick start](#quick-start)
    - [Requirements](#requirements)
    - [Reference](#reference)
    - [Version](#version)
    - [Adding ICON SDK for Python](#adding-icon-sdk-for-python)
    - [Creating an IconService instance and Setting a provider](#creating-an-iconservice-instance-and-setting-a-provider)
  - [Querying API methods](#querying-api-methods)
    - [Examples](#examples)
    - [Error cases](#error-cases)
    - [get_block](#get_block)
      - [Parameters](#parameters)
      - [Returns](#returns)
      - [Example](#example)
    - [get_balance](#get_balance)
      - [Parameters](#parameters-1)
      - [Returns](#returns-1)
      - [Example](#example-1)
    - [get_score_api](#get_score_api)
      - [Parameters](#parameters-2)
      - [Returns](#returns-2)
      - [Example](#example-2)
    - [get_total_supply](#get_total_supply)
      - [Parameters](#parameters-3)
      - [Returns](#returns-3)
      - [Example](#example-3)
    - [get_transaction](#get_transaction)
      - [Parameters](#parameters-4)
      - [Returns](#returns-4)
      - [Example](#example-4)
    - [get_transaction_result](#get_transaction_result)
      - [Parameters](#parameters-5)
      - [Returns](#returns-5)
      - [Example](#example-5)
    - [call](#call)
      - [Parameters](#parameters-6)
      - [Returns](#returns-6)
      - [Example](#example-6)
  - [Loading a wallet and storing the keystore](#loading-a-wallet-and-storing-the-keystore)
    - [Examples](#examples-1)
  - [API methods of KeyWallet](#api-methods-of-keywallet)
    - [create](#create)
      - [Parameters](#parameters-7)
      - [Returns](#returns-7)
      - [Example](#example-7)
    - [load](#load)
      - [Parameters](#parameters-8)
      - [Returns](#returns-8)
      - [Example](#example-8)
    - [load](#load-1)
      - [Parameters](#parameters-9)
      - [Returns](#returns-9)
      - [Example](#example-9)
    - [store](#store)
      - [Parameters](#parameters-10)
      - [Returns](#returns-10)
      - [Example](#example-10)
    - [get_address](#get_address)
      - [Parameters](#parameters-11)
      - [Returns](#returns-11)
      - [Example](#example-11)
    - [get_private_key](#get_private_key)
      - [Parameters](#parameters-12)
      - [Returns](#returns-12)
      - [Example](#example-12)
    - [sign](#sign)
      - [Parameters](#parameters-13)
      - [Returns](#returns-13)
      - [Example](#example-13)
  - [Signing and Sending transaction](#signing-and-sending-transaction)
    - [Generating a transaction](#generating-a-transaction)
    - [Signing a transaction](#signing-a-transaction)
    - [Sending a transaction](#sending-a-transaction)
    - [Examples](#examples-2)
    - [TransactionBuilder](#transactionbuilder)
      - [set methods](#set-methods)
      - [Returns](#returns-14)
      - [Example](#example-14)
    - [DeployTransactionBuilder](#deploytransactionbuilder)
      - [methods](#methods)
      - [Returns](#returns-15)
      - [Example](#example-15)
    - [CallTransactionBuilder](#calltransactionbuilder)
      - [methods](#methods-1)
      - [Returns](#returns-16)
      - [Example](#example-16)
    - [MessageTransactionBuilder](#messagetransactionbuilder)
      - [methods](#methods-2)
      - [Returns](#returns-17)
      - [Example](#example-17)
    - [SignedTransaction](#signedtransaction)
      - [Parameters](#parameters-14)
      - [Returns](#returns-18)
      - [Example](#example-18)
    - [send_transaction](#send_transaction)
      - [Parameters](#parameters-15)
      - [Returns](#returns-19)
      - [Example](#example-19)

<!-- /TOC -->

## Quick start

### Requirements

ICON SDK for Python development and execution requires following environments.

- Python
    - Version: Python 3.6+
    - IDE: Pycharm is recommended.

### Reference
- [ICON JSON-RPC API v3](https://github.com/icon-project/icon-rpc-server/blob/master/docs/icon-json-rpc-v3.md)
- [ICON SDK for Python(Previous version)](https://github.com/icon-project/icon_sdk_for_python)
    - Reference to [ICON JSON-RPC API **v2**](https://github.com/icon-project/icx_JSON_RPC)

### Version

1.0.5 beta

### Adding ICON SDK for Python

First you need to get ICON SDK for Python into your project. This can be installed using pip as follows:

``````shell
$ pip install iconsdk
``````

### Creating an IconService instance and Setting a provider

After that, you need to create an IconService instance and set a provider.

- The **IconService** class contains a set of API methods. It accepts a HTTPProvider which serves the purpose of connecting to HTTP and HTTPS based JSON-RPC servers.

- A **provider** defines how the IconService connects to Loopchain.

- The **HTTPProvider** takes the full URI where the server can be found. For local development, this would be something like http://localhost:9000.

Here is an example of a simple API method call for getting a block by its height:

```python
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

# Creates an IconService instance using the HTTP provider and set a provider.
icon_service = IconService(HTTPProvider("https://iconx.io"))

# Gets a block by a given block height.
block = icon_service.get_block(1209)
```



## Querying API methods

### Examples

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

# Generates a call instance using the CallBuilder
call = CallBuilder().from_(wallet.get_address())\
                    .to("cx000...1")\
                    .method("balance_of")\
                    .params({"address": "hx000...1"})\
                    .build()

# Executes a call method to call a read-only API method on the SCORE immediately without creating a transaction on Loopchain
result = icon_service.call(call)

```



### Error cases

There are different types of error case as follows.  The exception is raised with the specific message. You can get more info about the exception from the message.   

- **KeyStoreException** 
  - It is raised when making or loading a key store file.  
  - Error code for the exception is 1. 

- **AddressException**
  - It is raised when the address is invalid. 
  - Error code for the exception is 2. 

- **BalanceException**
  - It is raised when the balance is invalid.
  - Error code for the exception is 3. 
- **DataTypeException**
  - It is raised when the data type is invalid.
  - Error code for the exception is 4. 

- **JSONRPCException**
  - It is raised when JSON-RPC response is an error.  
  - Error code for the exception is 5. 

- **ZipException**
  - It is raised while writing zip in memory.
  - Error code for the exception is 6. 



### get_block

``````python
get_block(value)
``````

* Function A
  -  Returns block information by block height
  -  Delegates to **icx_getBlockByHeight** RPC method

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

#### Error cases

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
get_balance(address: str)
```

Returns the ICX balance of the given EOA or SCORE

Delegates to **icx_getBalance** RPC method

#### Parameters

address : An address of EOA or SCORE

#### Returns

Number of ICX coins

#### Error cases

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
get_score_api(address: str)
```

Returns SCORE's external API list

Delegates to **icx_getScoreApi** RPC method

#### Parameters

address : A SCORE address to be examined

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

#### Error cases

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
get_total_supply()
```

Returns total ICX coin supply that has been issued

Delegates to **icx_getTotalSupply** RPC method

#### Parameters

None

#### Returns

Total number of ICX coins issued

#### Error cases

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

#### Error cases

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

#### Error cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Returns the transaction result requested by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000")
```



### call

```python
call(call: Call)
```

Calls SCORE's external function which is read-only without creating a transaction on Loopchain

Delegates to **icx_call** RPC method

#### Parameters

Call object made by **CallBuilder**

Fields :

* from : Message sender's address
* to : A SCORE address that will handle the message
* method : name of an external function
* params : Parameters to be passed to the function (optional). A data type of params should be **dict**.


#### Returns

Values returned by the executed SCORE function

#### Error cases

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

# Calls SCORE's external function which is read-only without creating a transaction on Loopchain
result = icon_service.call(call)
```



## Loading a wallet and storing the keystore

To send transactions, first, you should make an instance of your wallet.  

You can make an instance of the wallet using bytes of the private key or from a keystore file.

### Examples

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



## API methods of KeyWallet

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

``````python
# Generates a wallet
wallet = KeyWallet.create()
``````



### load

```python
load(private_key: bytes)
```

Loads a wallet from bytes of the private key and generates an instance of Wallet

#### Parameters

private_key : Bytes of the private key

#### Returns

An instance of Wallet class

#### Error cases

* DataTypeException : Private key is invalid.

#### Example

```python
# Loads a wallet from bytes of the private key
wallet = KeyWallet.load(b'-B\x99...xedy')
```



### load

```python
load(file_path, password)
```

Loads a wallet from a keystore file with your password and generates an instance of Wallet

#### Parameters

* file_path : File path of the keystore file

* password : Password for the keystore file. Password must include alphabet character, number, and special character

#### Returns

An instance of Wallet class

#### Error cases

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

#### Error cases

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

#### Error cases

* DataTypeException : Data type is invalid.

#### Example

``` python
# Signs the transaction
signature = wallet.sign(b'D8\xe9...\xfc')
```



## Signing and Sending transaction

### Generating a transaction

After then, you should create an instance of the transaction using different types of **transaction builders** as follows.  

### Signing a transaction

Before sending a transaction, the transaction should be signed by using **SignedTransaction** class. The SignedTransaction class is used to sign the transaction by returning an instance of the signed transaction as demonstrated in the example below. The instance of the signed transaction has the property of a signature.  

### Sending a transaction

Finally, you can send a transaction with the signed transaction object as follows.

### Examples

```python
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
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
    .data("test")\
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
- data : Data by the dataType. Data type of the data should be **string**.
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
    .data("test")\
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

#### Error cases

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

Need to wait for a while after sending the transaction. Because it takes time to make a consensus among nodes. We recommend 0.3 second at least.

#### Parameters

signed_transaction : A signed transaction object

#### Returns

Transaction hash prefixed with '0x'

#### Error cases

* DataTypeException : Data type is invalid.
* JSONRPCException :  JSON-RPC Response is error.

#### Example

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```
