# Introduction 

This document describes how to use ICON SDK for Python including code snippets and API references.



## Quick start

A simple querying API, getting a block matching the given block's height is as follows.

```python
icon_service = IconService(HttpProvider("https://iconx.io"));

# Gets a block matching the block height.
block = iconService.getBlock(1209);
```



## IconService 

APIs can be called through [IconService ](#class-iconservice)initialized as follows.

```python
# Creates an instance of IconService using the HTTP provider.
icon_service = IconService(HttpProvider("https://iconx.io", request_kwargs={'timeout': 60}));
```



## Querying APIs

Every querying APIs supports not asynchronous executions but `synchronous` executions.

It can be called as follows.

```python
# Gets the block
block = icon_service.get_block(1000)    # by height

block = icon_service.get_block("0x000...000")    # by hash

block = icon_service.get_block("latest")    # latest block
    
# Gets the balance of an given account
balance = icon_service.get_balance("hx000...1")

# Gets a list of the SCORE API
score_apis = icon_service.get_score_api("cx000...1")

# Gets total supply of icx
total_supply = icon_service.get_total_supply()

# Gets a transaction matching the given transaction hash
tx = icon_service.get_transaction("0x000...000")

# Gets the result of the transaction matching the given transaction hash
tx_result = icon_service.get_transaction_result("0x000...000");

# Calls a SCORE API which is read-only
call = CallBuilder().from(wallet.get_address())		\
					.to("cx00")						\
					.method("transfer")				\
					.params(params)					\
            		.build()
result = icon_service.call(call)

```



## Send a transaction

**Loading wallets and storing the keystore**

First of all, if you want to send transactions, you should make an instance of your wallet. 

You can make an instance of the wallet using a private key or from a keystore file. 

```python
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
wallet.sign_message("0xc7130...238")
```

**Creating an instance of transaction**

If you want to send a transaction, you should create an instance of transaction using builder as follows.

```python
# Makes an instance of transaction for sending icx.
raw_transaction = IcxTransactionBuilder()			\
    .from(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(BigInteger("150000000"))					\
    .stepLimit(BigInteger("1000000"))				\
    .nonce(BigInteger("1000000"))					\
    .build()

# Makes an instance of transation for deploying SCORE.
raw_transaction = DeployTransactionBuilder()		\
    .from(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(BigInteger("150000000"))					\
    .stepLimit(BigInteger("1000000"))				\
    .nonce(BigInteger("1000000"))					\
    .contentType("application/zip")					\
    .content(inputStream)							\
    .params(params)									\
    .build()

# Makes an instance of transation for calling method in SCORE.
raw_transaction = CallTransactionBuilder()			\
    .from(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(BigInteger("150000000"))					\
    .stepLimit(BigInteger("1000000"))				\
    .nonce(BigInteger("1000000"))					\
    .method("transfer")								\
    .params(params)									\
	.build()
    
# Makes an instance of transation for sending a message.
raw_transaction = MessageTransactionBuilder()		\
    .from(wallet.getAddress())						\
    .to("cx00...02")								\
    .value(BigInteger("150000000"))					\
    .stepLimit(BigInteger("1000000"))				\
    .nonce(BigInteger("1000000"))					\
    .data(inputStream)								\
    .build()
```

**Signing a transaction**

Before sending a transaction, the transaction should be signed. 

`SignedTransaction` is used to sign the transaction returning an instance of the signed transaction as follows. The instance of the signed transaction has property of signiture. 

```python
signed_transaction = SignedTransaction(raw_transaction, wallet)
```

**Sending a transaction**

Finally, you can send a transation as follows.

```python
result = send_transaction(signed_transaction)
```



# APIs

## class IconService

Calls APIs of ICON JSON RPC

### Method

#### get_block(height: int)

Equivalent to `icx_getGetBlockByHeight`

#### get_block(blockHash: str)

Equivalent to `icx_getGetBlockByHash`

#### get_block("lastest")

Equlvalent to `icx_getLastBlock`

#### get_total_supply()

Equivalent to `icx_getTotalSupply`

#### get_balance(address: str)

Equivalent to `icx_getBalance`

#### get_score_api(address: str)

Equivalent to `icx_getScoreApi`

#### get_transaction_result(txHash: str)

Equivalent to `icx_getTransactionResult`

#### get_transaction(txHash: str)

Equivalent to `icx_getTransactionByHash`

#### call(call: object)

Equivalent to `icx_call`

#### send_transaction(signed_transaction: object)

Equivalent to `icx_sendTransaction`



## Interface class Wallet

### Method

#### get_address()

#### sign_message(hash: str) -> str



## class KeyWallet(Wallet)

### Method

#### create()

#### load(private_key: str)

#### load(path: str, password: str)

#### store(path: str, password: str)

#### get_private_key()



## class Call

### properties

- from_: str
- to_: str
- method: str
- params: dict

## class CallBuilder() -> Call

### method 

#### from(from_: str)

#### to(to_: str)

#### method(method: str)

#### params(params: dic)

#### build()



## Abstract Class Transaction

[IcxTransaction](#class-icxtransaction-implements-transaction), [CallTransaction](#class-calltransaction-implements-transaction), [DeployTransaction](#class-deploytransaction-implements-transaction), [MessageTransaction](#class-messagetransaction-implements-transaction)
### properties
- from_: str
- to_: str
- value: int
- stepLimit: int
- nonce: int
- version: int
- timeStamp: long
- dataType: str

### method 
#### serialize(from_: str)



## Abstract Class Builder

### method

#### from(from_: str)

#### to(to_: str)

#### value(value: int)

#### stepLimit(stepLimit: int)

#### nonce(nonce: int)

#### version(version: int)

#### timeStamp(timeStamp: long)

#### dataType(dataType: str)



## Class IcxTransaction(Transaction)

## class IcxTransactionBuilder(Builder) -> IcxTransaction



## Class CallTransaction(Transaction)

### properties 
- method: str
- params: dict

## class CallTransactionBuilder(Builder) -> CallTransaction

### method

#### method(method: str)

#### params(params: dict)



## Class DeployTransaction(Transaction)

### properties

- content_type: str
- content: str 
- params: dict

## class DeployTransactionBuilder(Builder) -> DeployTransaction

### method

#### content_type(content_type: str)

#### content(content: str)

#### params(params: dict)



## Class MessageTransaction(Transaction)

### properties

- message: str

## class MessageTransactionBuilder(Builder) -> MessageTransaction

### method

#### message(message: str)



## class SignedTransaction(Transaction)

### properties

* Signature: str

### Methods

#### getParams() -> dict

#### serialize(param: dict) -> str 



## abstract class Provider

## class HttpProvider(Provider)


