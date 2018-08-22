 

# Introduction 

ICON SDK for Python is a collection of libraries which allow you to interact with a local or remote Loopchain node, using an HTTP connection. The following documentation will guide you through installing and running ICON SDK for Python as well as providing an API reference documentation examples.



## Quick start 

### Prerequisite

Python 3.6.x 

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
# Returns information about a block by block height
block = icon_service.get_block(1000)    		 

# Returns information about a block by hash
block = icon_service.get_block("0x000...000")

# Returns information about the latest block
block = icon_service.get_block("latest")    	
    
# Returns the balance of the account of given address
balance = icon_service.get_balance("hx000...1")

# Returns a list of the SCORE APIs
score_apis = icon_service.get_score_api("cx000...1")

# Returns the total supply of ICX
total_supply = icon_service.get_total_supply()

# Returns the information about a transaction requested by transaction hash
tx = icon_service.get_transaction("0x000...000")

# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000");

# Creates a call instance using the CallBuilder 
call = CallBuilder().from_(wallet.get_address())		\
					.to("cx000...1")					\
					.method("balance_of")				\
					.params(params)						\
            		.build()
# Executes a call which is a read-only SCORE API immediately without creating a transaction on the blockchain
result = icon_service.call(call)

```

### get_block(value)

* Funtion A 
  -  Returns information about a block by block height
  - Delegates to **icx_getBlockByHeight** RPC method

* Funtion B 
  * Returns information about a block by hash
  * Delegates to **icx_getBlockByHash** RPC method

* Funtion C
  * Returns information about the latest block
  * Delegates to **icx_getLastBlock** RPC method

#### Parameters

* Funtion A 
  * Value : Block height which is an integer
* Function B
  * Value : Block hash prefixed with '0x' 
* Funtion C
  - Value : 'latest'

#### Returns

A block object

#### Example

```python
# Returns information about a block by block height
block = icon_service.get_block(1000)    		 

# Returns information about a block by hash
block = icon_service.get_block("0x000...000")

# Returns information about the latest block
block = icon_service.get_block("latest")  
```

### 

### get_balance(address: str)

Returns the balance of the account of given address

Delegates to **icx_getBalance** RPC method

#### Parameters

address: An address of the account prefixed with 'hx' 

#### Returns

The current balance of the account in loop which is an integer

#### Example

```python
# Returns the balance of the account of given address
balance = icon_service.get_balance("hx000...1")
```

### 

### get_score_api()

Returns a list of API methods of the SCORE

Delegates to **icx_getScoreApi** RPC method

#### Parameters

None

#### Returns

A list of API methods of the SCORE and its information

Fields :

* type : Function, fallback, on_install, on_update, eventlog
* name : An API method's name on the SCORE
* inputs : A list of information of parameters
  * name : Parameter's name
  * type : Parameter's type
  * indexed : If the method is eventlog, it is used.
* outputs : Information on the returns 
  * type : The returns' type
* Readonly : If the method is external method, readonly is True
* Payable: Payable

#### Example

```python
# Returns a list of the SCORE APIs
score_apis = icon_service.get_score_api("cx000...1")
```

### 

### get_total_supply()

Returns the total supply of ICX

Delegates to **icx_getTotalSupply** RPC method

#### Parameters

None

#### Returns

The total supply of ICX in loop which is an integer

#### Example

```python
# Returns the total supply of ICX
total_supply = icon_service.get_total_supply()
```

### 

### get_transaction(tx_hash: str)

Returns the information about a transaction requested by transaction hash

Delegates to **icx_getTransactionByHash** RPC method

#### Parameters

tx_hash : Transaction hash prefixed with '0x' 

#### Returns

Information about a transaction 

Field : 

- version : The verion of protocol ("0x3" for V3)
- from : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- value :  The amount of ICX to be sent
- stepLimit :  The maximum step value for processing a transaction
- timestamp: A timestamp when sending a transaction
- nid: Network ID
- nonce: A random integer for transaction hash prevention
- txHash: Transaction hash
- txIndex: Transaction index in a block. It will be null when it is pending
- blockHeight : Block height having the transaction. It will be null when pending
- blockHash: Block Hash having the transaction. It will be null when pending
- signature: Digital signature for the transaction
- dataType: Data type; call, deploy, message
- data: Data by the dataType

#### Example

```python
# Returns the information about a transaction requested by transaction hash
tx = icon_service.get_transaction("0x000...000")
```



### get_transaction_result(tx_hash: str)

Returns the result of a transaction by transaction hash

Delegates to **icx_getTransactionResult** RPC method

#### Parameters

tx_hash : Hash of a transaction prefixed with '0x' 

#### Returns

A transaction result object 

Field : 

* status : 1(success), 0(failure)
* to : The wallet address to receive coin or SCORE address  to receive a transaction
* failure : If the status is 0 when failing, failure has dictionary type data having fields, the code in a string and message in a string
* txHash :  transaction hash
* txIndex: transaction index in a block
* blockHeight : Block height having the transaction
* blockHash: Block Hash having the transaction
* cumulativeStepUsed: Digital signature for the transaction
* stepUsed: Data type; call, deploy, message
* stepPrice: Data by the dataType
* scoreAddress : The SCORE address when the transaction installing SCORE (optional)
* eventLogs : A list of EventLog while processing the transaction
* logsBloom : The Bloom filter value of an indexed data of a happened EventLog Data

#### Example

```python
# Returns the result of a transaction by transaction hash
tx_result = icon_service.get_transaction_result("0x000...000");
```



### call(call)

Executes a call which is a read-only external SCORE API method immediately without creating a transaction on the blockchain

Delegates to **icx_call** RPC method

#### Parameters

Call object made by CallBuilder

Fields : 

*  from : The wallet address to execute a call which is a read-only external SCORE API method

* to : The SCORE address 

* method : The read-only external SCORE API method

* params : Parameters of the method (optional)


#### Returns

Object : Returns executing the call 

#### Example

```python
# Creates a call instance using the CallBuilder 
call = CallBuilder().from_(wallet.get_address())		\
					.to("cx000...1")					\
					.method("balance_of")				\
					.params(params)						\
            		.build()
# Executes a call which is a read-only SCORE API immediately without creating a transaction on the blockchain
result = icon_service.call(call)
```

### 

## Loading a wallet and storing the keystore

To send transactions, first, you should make an instance of your wallet.  

You can make an instance of the wallet using a private key or from a key store file. 

### Examples

```python
from IconService.wallet.wallet import KeyWallet

# Generates a wallet.
wallet = KeyWallet.create()

# Loads a wallet from a private key.
wallet = KeyWallet.load("0x0000")

# Loads a wallet from a key store file.
wallet = KeyWallet.load("./key.keystore", "password")

# Stores  a keystore file on the file path.
wallet.store("./new.keystore", "password") # throw exception if having an error.

# Gets an Address.
wallet.get_address()

# Get a private key.
wallet.get_private_key()

# Signs message.
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
# Generates a wallet.
wallet = KeyWallet.create()
``````

### 

### load(hex_private_key: str) 

Loads a wallet from a private key and generates an instance of Wallet

#### Parameters

hex_private_key : A private key in hexadecimal - 256 bits in hexadecimal is 32 bytes, or 64 characters in the range 0-9 or A-F. A tiny bit of code that is paired with a public key to set off algorithms to encrypt and decrypt a text for the specific address

#### Returns

An instance of Wallet class

#### Example

```python
# Loads a wallet from a private key.
wallet = KeyWallet.load("0x0000")
```

### 

### load(file_path, password) 

Loads a wallet from a key store file with a password and generates an instance of Wallet

#### Parameters

* File_path : The file path for the key store file of the wallet

- password : Password for the wallet. Password must include alphabet character, number, and special character

#### Returns

An instance of Wallet class

#### Example

```python
# Loads a wallet from a key store file.
wallet = KeyWallet.load("./key.keystore", "password")
```

### 

### store(file_path, password)

Stores data of an instance of a derived wallet class on the file path with your password

#### Parameters

- File_path : File path for the keystore file of the wallet
- password :  Password for the wallet. Password must include alphabet character, number, and special character

#### Returns

None

#### Example

```python
# Stores a keystore file on the file path.
wallet.store("./new.keystore", "password") # throw exception if having an error.
```



### get_address()

Returns a wallet address of wallet which starts with 'hx'

#### Parameters

None

#### Returns

String of wallet address begins from ‘hx’.

#### Example

```python
# Gets an Address.
wallet.get_address()
```

### 

### get_private_key() 

Returns a private key of an instance of a derived wallet class

#### Parameters

None

#### Returns

A private_key in hexadecimal

#### Example

```python
# Get a private key.
wallet.get_private_key()
```

### 

### sign_message(message_hash: bytes)

Returns on ECDSA-SHA256 signature in bytes using massage hash

#### Parameters

message_hash : Message hash in bytes

#### Returns

Signature in bytes

#### Example

``` python
# Signs message.
signature = wallet.sign_message(b'D8\xe9...\xfc')
```



## Creating an instance of transaction

### Generating a transaction

After then, you should create an instance of the transaction using different types of **transaction builders** as follows.  

### Signing a transaction 

Before sending a transaction, the transaction should be signed by using **SignedTransaction** class. The SignedTransaction class is used to sign the transaction returning an instance of the signed transaction as follows. The instance of the signed transaction has the property of a signature.  

### Sending a transaction 

Finally, you can send a transaction with the signed transaction object as follows.

### Examples

```python
from IconService.builder.transaction_builder import IcxTransactionBuilder, DeployTransactionBuilder, CallTransactionBuilder, MessageTransactionBuilder
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

Builder for **Transaction** object

#### set methods

* from_ : the wallet address making a transaction 
* to : The wallet address to receive coin or SCORE address  to receive a transaction
* value : The amount of ICX to be sent
* step_limit : The maximum step value for processing a transaction
* nid : Network ID
* nonce : A random integer for transaction hash prevention
* build : Returns an ICX transaction object  

#### Returns

An transaction object  

#### Example

```python
# Makes an instance of transaction for sending icx.
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
- nonce :  A random integer for transaction hash prevention
- content_type : Content's mime-type
- content : Binary data of the SCORE
- params : Parameters passed on the SCORE methods as like on_install () and on_update () (optional)
- build : Returns a deploy transaction object  

#### Returns

A deploy transaction object  

#### Example

```python
# Makes an instance of transation for deploying SCORE.
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

### 

### CallTransactionBuilder

Builder for **CallTransaction** object

#### methods

- from_ : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- step_limit : The maximum step value for processing a transaction
- nid : Network ID
- nonce : A random integer for transaction hash prevention
- method : Methods in the SCORE
- params : Parameters passed on the SCORE methods (optional)
- Build : Returns a call transaction object  

#### Returns

A call transaction object  

#### Example

```python
# Makes an instance of transation for calling method in SCORE.
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

### 

### MessageTransactionBuilder

Builder for **MessageTransaction** object

#### methods

- from_ : The wallet address making a transaction 
- to : The wallet address to receive coin or SCORE address  to receive a transaction
- stepLimit : The maximum step value for processing a transaction
- nid : Network ID
- nonce : A random integer for transaction hash prevention
- data : Data by the dataType
- build : Returns a message transaction object  

#### Returns

A message transaction object  

#### Example

```python
# Makes an instance of transation for sending a message.
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

#### Parameters

signed_transaction : The signed transaction object having a signature field finally

#### Returns

The transaction hash prefixed with '0x'

#### Example

```python
# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
```

