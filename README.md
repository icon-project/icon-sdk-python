  

# ICON SDK for Python

ICON SDK for Python is a collection of libraries which allow you to interact with a local or remote Loopchain node, using an HTTP connection. The following documentation will guide you through installing and running ICON SDK for Python as well as providing an API reference documentation examples.



## Quick start 

### Prerequisite

Python 3.6.x 

### Version

0.0.1 beta

### Adding ICON SDK for Python 

First you need to get ICON SDK for Python into your project. This can be installed using pip as follows:

``````shell
$ pip install icon-sdk-python
``````

### Creating an IconService instance and Setting a provider 

After that, you need to create an IconService instance and set a provider. 

- The **IconService** class contains the following API methods. It comes with the HttpProvider, the built-in provider, which is for connecting to HTTP and HTTPS based JSON-RPC servers. 

- The **provider** is how IconService connects to Loopchain.

- The **HTTPProvider** takes the full URI where the server can be found. For local development this would be something like http://localhost:9000.

 A simple API method getting a block matching the given block's height is as follows.

```python
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider

# Creates an IconService instance using the HTTP provider and set a provider.
icon_service = IconService(HttpProvider("https://iconx.io"));

# Gets a block matching the block height.
block = icon_service.getBlock(1209);
```



## Querying API methods

### Examples

```python
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
tx_result = icon_service.get_transaction_result("0x000...000");

# Generates a call instance using the CallBuilder 
call = CallBuilder().from_(wallet.get_address())		\
					.to("cx000...1")					\
					.method("balance_of")				\
					.params(params)						\
            		.build()
# Executes a call method to call a read-only API method on the SCORE immediately without creating a transaction on Loopchain
result = icon_service.call(call)

```



### get_block(value)

* Function A 
  -  Returns block information by block height
  - Delegates to **icx_getBlockByHeight** RPC method

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
  - value : 'latest'

#### Returns

Block data

#### Example

```python
# Returns block information by block height
block = icon_service.get_block(1000)    		 

# Returns block information by block hash
block = icon_service.get_block("0x000...000")

# Returns the last block information
block = icon_service.get_block("latest")  
```



### get_balance(address: str)

Returns the ICX balance of the given EOA or SCORE

Delegates to **icx_getBalance** RPC method

#### Parameters

address : An address of EOA or SCORE prefixed with 'hx' 

#### Returns

Number of ICX coins

#### Example

```python
# Returns the ICX balance of the given EOA or SCORE
balance = icon_service.get_balance("hx000...1")
```



### get_score_api(address: str)

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

#### Example

```python
# Returns SCORE's external API list
score_apis = icon_service.get_score_api("cx000...1")
```



### get_total_supply()

Returns total ICX coin supply that has been issued

Delegates to **icx_getTotalSupply** RPC method

#### Parameters

None

#### Returns

Total number of ICX coins issued

#### Example

```python
# Returns total ICX coin supply that has been issued
total_supply = icon_service.get_total_supply()
```



### get_transaction(tx_hash: str)

Returns the transaction information requested by transaction hash

Delegates to **icx_getTransactionByHash** RPC method

#### Parameters

tx_hash : Transaction hash prefixed with '0x' 

#### Returns

Information about a transaction 

Field : 

- version : Protocol version ("0x3" for V3)
- from : An EOA address that created the transaction
- to : An EOA address to receive coins, or SCORE address to execute the transaction
- value : Amount of ICX coins in loop to transfer. When omitted, assumes 0. (1 icx = 1 ^ 18 loop)
- stepLimit :  Maximum step allowance that can be used by the transaction
- timestamp : Transaction creation time. timestamp is in the microsecond
- nid : Network ID
- nonce : An arbitrary number used to prevent transaction hash collision
- txHash : Transaction hash
- txIndex : Transaction index in a block. Null when it is pending.
- blockHeight : Block height where this transaction was in. Null when it is pending
- blockHash : Block Hash where this transaction was in. Null when it is pending.
- signature : Signature of the transaction
- dataType : Data type; call, deploy, message
- data : Contains various type of data depending on the dataType

#### Example

```python
# Returns the transaction information requested by transaction hash
tx = icon_service.get_transaction("0x000...000")
```



### get_transaction_result(tx_hash: str)

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
* txHash :  Transaction hash
* txIndex: Transaction index in the block
* blockHeight : Block height including the transaction
* blockHash: Block Hash including the transaction
* cumulativeStepUsed: Sum of stepUsed by this transaction and all preceeding transactions in the same block
* stepUsed: The amount of step used by this transaction
* stepPrice: The step price used by this transaction
* scoreAddress : A SCORE address if the transaction created a new SCORE. (optional)
* eventLogs : Array of eventlogs, which this transaction generated
* logsBloom : Bloom filter to quickly retrieve related eventlogs

#### Example

```python
# Returns the transaction result requested by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000");
```



### call(call)

Calls SCORE's external function which is read-only without creating a transaction on Loopchain

Delegates to **icx_call** RPC method

#### Parameters

Call object made by **CallBuilder**

Fields : 

* from : Message sender's address

* to : A SCORE address that will handle the message

* method : name of an external function

* params : Parameters to be passed to the function (optional)


#### Returns

Values returned by the executed SCORE function

#### Example

```python
# Creates a call instance using the CallBuilder 
call = CallBuilder().from_(wallet.get_address())		\
					.to("cx000...1")					\
					.method("balance_of")				\
					.params(params)						\
            		.build()
# Calls SCORE's external function which is read-only without creating a transaction on Loopchain
result = icon_service.call(call)
```



## Loading a wallet and storing the keystore

To send transactions, first, you should make an instance of your wallet.  

You can make an instance of the wallet using a private key or from a key store file. 

### Examples

```python
from IconService.wallet.wallet import KeyWallet

# Generates a wallet
wallet = KeyWallet.create()

# Loads a wallet from a private key
wallet = KeyWallet.load("0x0000")

# Loads a wallet from a key store file
wallet = KeyWallet.load("./key.keystore", "password")

# Stores a keystore file on the file path
wallet.store("./new.keystore", "password") # throw exception if having an error.

# Returns an Address
wallet.get_address()

# Returns a private key
wallet.get_private_key()

# Signs message
signature = wallet.sign_message(b'D8\xe9...\xfc')
```



## API methods of KeyWallet

### create()

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



### load(hex_private_key: str) 

Loads a wallet from a private key and generates an instance of Wallet

#### Parameters

hex_private_key : A private key in hexadecimal - 256 bits in hexadecimal is 32 bytes, or 64 characters in the range 0-9 or A-F. A tiny bit of code that is paired with a public key to set off algorithms to encrypt and decrypt a text for the specific address

#### Returns

An instance of Wallet class

#### Example

```python
# Loads a wallet from a private key
wallet = KeyWallet.load("0x0000")
```



### load(file_path, password) 

Loads a wallet from a key store file with your password and generates an instance of Wallet

#### Parameters

- File_path : File path of the key store file 

- password : Password for the key store file. Password must include alphabet character, number, and special character

#### Returns

An instance of Wallet class

#### Example

```python
# Loads a wallet from a key store file
wallet = KeyWallet.load("./key.keystore", "password")
```



### store(file_path, password)

Stores data of an instance of a derived wallet class on the file path with your password

#### Parameters

- File_path : File path of the key store file

- password :  Password for the key store file. Password must include alphabet character, number, and special character

#### Returns

None

#### Example

```python
# Stores a keystore file on the file path
wallet.store("./new.keystore", "password") # throw exception if having an error.
```



### get_address()

Returns  an EOA address 

#### Parameters

None

#### Returns

 An EOA address

#### Example

```python
# Returns an EOA address 
wallet.get_address()
```



### get_private_key() 

Returns the private key of the wallet

#### Parameters

None

#### Returns

The private key in hexadecimal

#### Example

```python
# Returns the private key
wallet.get_private_key()
```



### sign_message(message_hash: bytes)

Returns on ECDSA-SHA256 signature in bytes using massage hash

#### Parameters

message_hash : Message hash in bytes

#### Returns

Signature in bytes

#### Example

``` python
# Signs message
signature = wallet.sign_message(b'D8\xe9...\xfc')
```



## Creating an instance of transaction

### Generating a transaction

After then, you should create an instance of the transaction using different types of **transaction builders** as follows.  

### Signing a transaction 

Before sending a transaction, the transaction should be signed by using **SignedTransaction** class. The SignedTransaction class is used to sign the transaction by returning an instance of the signed transaction as follows. The instance of the signed transaction has the property of a signature.  

### Sending a transaction 

Finally, you can send a transaction with the signed transaction object as follows.

### Examples

```python
from IconService.builder.transaction_builder import (
	IcxTransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from IconService.signed_transaction import SignedTransaction

# Generates an instance of transaction for sending icx.
raw_transaction = IcxTransactionBuilder()			\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(150000000)								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .build()

# Generates an instance of transation for deploying SCORE.
raw_transaction = DeployTransactionBuilder()		\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .content_type("application/zip")				\
    .content(b'D8\xe9...\xfc')						\
    .params(params)									\
    .build()

# Generates an instance of transation for calling method in SCORE.
raw_transaction = CallTransactionBuilder()			\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .method("balance_of")							\
    .params(params)									\
	.build()
    
# Generates an instance of transation for sending a message.
raw_transaction = MessageTransactionBuilder()		\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .data("test")								    \
    .build()

# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(raw_transaction, wallet)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```



### IcxTransactionBuilder

Builder for a **Transaction** object

#### set methods

* from_ : the wallet address making a transaction 
* to : The wallet address to receive coin or SCORE address  to receive a transaction
* value : The amount of ICX to be sent
* step_limit : The maximum step value for processing a transaction
* nid : Network ID
* nonce :  An arbitrary number used to prevent transaction hash collision
* build : Returns an ICX transaction object  

#### Returns

A transaction object  

#### Example

```python
# Generates an instance of transaction for sending icx.
raw_transaction = IcxTransactionBuilder()			\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(150000000)								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .build()
```



### DeployTransactionBuilder

Builder for **DeployTransaction** object

#### methods

- from_ : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- step_limit : The maximum step value for processing a transaction
- nid : Network ID
- nonce :   An arbitrary number used to prevent transaction hash collision
- content_type : Content's mime-type
- content : Binary data of the SCORE
- params : Parameters passed on the SCORE methods ; on_install (), on_update () (optional)
- build : Returns a deploy transaction object  

#### Returns

A deploy transaction object  

#### Example

```python
# Generates an instance of transation for deploying SCORE.
raw_transaction = DeployTransactionBuilder()		\
	.from_(wallet.getAddress())						\
	.to("cx00...02")								\
	.step_limit(1000000)							\
	.nid(3)											\
	.nonce(100)										\
	.content_type("application/zip")				\
	.content(b'D8\xe9...\xfc')						\
	.params(params)									\
	.build()
```



### CallTransactionBuilder

Builder for **CallTransaction** object

#### methods

- from_ : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- step_limit : The maximum step value for processing a transaction
- nid : Network ID
- nonce :  An arbitrary number used to prevent transaction hash collision
- method : Methods in the SCORE
- params : Parameters passed on the SCORE methods (optional)
- Build : Returns a call transaction object  

#### Returns

A call transaction object  

#### Example

```python
# Generates an instance of transation for calling method in SCORE.
raw_transaction = CallTransactionBuilder()			\
    .from_(wallet.getAddress())						\
    .to("cx00...02")								\
    .step_limit(1000000)							\
    .nid(3)											\
    .nonce(100)										\
    .method("balance_of")							\
    .params(params)									\
	.build()
```



### MessageTransactionBuilder

Builder for **MessageTransaction** object

#### methods

- from_ : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- stepLimit : The maximum step value for processing a transaction
- nid : Network ID
- nonce :  An arbitrary number used to prevent transaction hash collision 
- data : Data by the dataType
- build : Returns a message transaction object  

#### Returns

A message transaction object  

#### Example

```python
# Generates an instance of transation for sending a message.
raw_transaction = MessageTransactionBuilder()		\
	.from_(wallet.getAddress())						\
	.to("cx00...02")								\
	.step_limit(1000000)							\
	.nid(3)											\
	.nonce(100)										\
	.data("test")								    \
	.build()
```



### SignedTransaction(transaction: Transaction, wallet: Wallet)

Returns the signed transaction object having a signature

#### Parameters

* transaction : A transaction object not having a signature field yet
* wallet : A wallet object 

#### Returns

The signed transaction object having a signature field finally

#### Example

```python
# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(raw_transaction, wallet)
```




### send_transaction(signed_transaction)

Sends the transaction

Delegates to **icx_sendTransaction** RPC method

#### Parameters

signed_transaction : The signed transaction object having a signature field finally

#### Returns

Transaction hash prefixed with '0x'

#### Example

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```

