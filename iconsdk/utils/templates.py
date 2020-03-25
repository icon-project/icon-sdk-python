from collections import namedtuple
from enum import Enum

from iconsdk.utils.convert_type import convert_hex_str_to_bytes, convert_hex_str_to_int


def addVersion(key, value, new_obj):
    new_obj[key] = value if value != '' else 2


def convert_data_content_to_bytes(key, value, new_obj):
    if new_obj["dataType"] == "deploy":
        new_obj[key]["content"] = convert_hex_str_to_bytes(value["content"])


def convert_failure_code_to_int(key, value, new_obj):
    if "failure" in new_obj:
        new_obj[key]["code"] = convert_hex_str_to_int(value["code"])


BLOCK_0_1A_VERSION = '0.1a'
BLOCK_0_3_VERSION = '0.3'

ConvertKeyName = namedtuple("ConvertKeyName", "new_key")
RemoveKey = namedtuple("RemoveKey", "")
ExceptionHandle = namedtuple("ExceptionHandle", "func")

funcAddVersion = addVersion
funcConvertDataContentToBytes = convert_data_content_to_bytes
funcConvertFailureCodeToBytes = convert_failure_code_to_int


class ValueType(Enum):
    none = 0
    str = 1
    int = 2
    bytes = 3
    list = 4
    dict = 5
    hex_hash_number = 6
    prefixed_hex_hash_number = 7


TRANSACTIONS_OF_BLOCK = [
    {
        "CHANGE": {
            "tx_hash": ConvertKeyName("txHash"),
            "method": RemoveKey(),
        },
        "version": ValueType.int,
        "from": ValueType.str,
        "to": ValueType.str,
        "value": ValueType.int,
        "fee": ValueType.int,
        "stepLimit": ValueType.int,
        "timestamp": ValueType.int,
        "nid": ValueType.int,
        "nonce": ValueType.int,
        "signature": ValueType.str,
        "txHash": ValueType.prefixed_hex_hash_number,
        "dataType": ValueType.str,
        "data": ValueType.dict
    }
]

TRANSACTIONS_OF_GENESIS_BLOCK = [
    {
        "accounts": ValueType.list,
        "message": ValueType.str,
        "nid": ValueType.int
    }
]

TRANSACTION = {
    "CHANGE": {
        "tx_hash": ConvertKeyName("txHash"),
        "method": RemoveKey(),
        "version": ExceptionHandle(funcAddVersion),
        "data": ExceptionHandle(funcConvertDataContentToBytes)
    },
    "version": ValueType.int,
    "from": ValueType.str,
    "to": ValueType.str,
    "value": ValueType.int,
    "fee": ValueType.int,
    "stepLimit": ValueType.int,
    "timestamp": ValueType.int,
    "nid": ValueType.int,
    "nonce": ValueType.int,
    "signature": ValueType.str,
    "txHash": ValueType.prefixed_hex_hash_number,
    "dataType": ValueType.str,
    "data": ValueType.dict,
    "txIndex": ValueType.int,
    "blockHeight": ValueType.int,
    "blockHash": ValueType.prefixed_hex_hash_number
}

TRANSACTION_RESULT = {
    "CHANGE": {
        "failure": ExceptionHandle(funcConvertFailureCodeToBytes)
    },
    "status": ValueType.int,
    "to": ValueType.str,
    "txHash": ValueType.prefixed_hex_hash_number,
    "txIndex": ValueType.int,
    "blockHeight": ValueType.int,
    "blockHash": ValueType.prefixed_hex_hash_number,
    "cumulativeStepUsed": ValueType.int,
    "stepUsed": ValueType.int,
    "stepPrice": ValueType.int,
    "eventLogs": ValueType.list,
    "logsBloom": ValueType.bytes,
    "failure": ValueType.dict,
    "scoreAddress": ValueType.str
}

PREV_VOTES = [
    {
        "rep": ValueType.str,
        "timestamp": ValueType.int,
        "blockHeight": ValueType.int,
        "blockHash": ValueType.hex_hash_number,
        "signature": ValueType.str
    }
]

LEADER_VOTES = [
    {
        "rep": ValueType.str,
        "timestamp": ValueType.int,
        "blockHeight": ValueType.int,
        "oldLeader": ValueType.str,
        "newLeader": ValueType.str,
        "signature": ValueType.str
    }
]

BLOCK_0_1a = {
    "version": ValueType.str,
    "prev_block_hash": ValueType.hex_hash_number,
    "merkle_tree_root_hash": ValueType.hex_hash_number,
    "time_stamp": ValueType.int,
    "confirmed_transaction_list": TRANSACTIONS_OF_BLOCK,
    "block_hash": ValueType.hex_hash_number,
    "height": ValueType.int,
    "peer_id": ValueType.str,
    "signature": ValueType.str,
    "next_leader": ValueType.str
}

BLOCK_0_3 = {
    "CHANGE": {
        "prev_block_hash": ConvertKeyName("prevHash"),
        "merkle_tree_root_hash": ConvertKeyName("transactionsHash"),
        "time_stamp": ConvertKeyName("timestamp"),
        "confirmed_transaction_list": ConvertKeyName("transactions"),
        "block_hash": ConvertKeyName("hash"),
        "peer_id": ConvertKeyName("leader"),
        "next_leader": ConvertKeyName("nextLeader"),
    },
    "version": ValueType.str,
    "hash": ValueType.prefixed_hex_hash_number,
    "prevHash": ValueType.prefixed_hex_hash_number,
    "prevVotesHash": ValueType.prefixed_hex_hash_number,
    "transactionsHash": ValueType.prefixed_hex_hash_number,
    "stateHash": ValueType.prefixed_hex_hash_number,
    "receiptsHash": ValueType.prefixed_hex_hash_number,
    "repsHash": ValueType.prefixed_hex_hash_number,
    "nextRepsHash": ValueType.prefixed_hex_hash_number,
    "leaderVotesHash": ValueType.prefixed_hex_hash_number,
    "logsBloom": ValueType.bytes,
    "timestamp": ValueType.int,
    "height": ValueType.int,
    "leader": ValueType.str,
    "nextLeader": ValueType.str,
    "signature": ValueType.str,
    "transactions": TRANSACTIONS_OF_BLOCK,
    "prevVotes": PREV_VOTES,
    "leaderVotes": LEADER_VOTES
}
