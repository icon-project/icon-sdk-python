from typing import Any, Dict, List, Optional, Union

# Import necessary components from iconsdk
from iconsdk.builder.call_builder import Call
from iconsdk.builder.transaction_builder import Transaction
from iconsdk.exception import AddressException, DataTypeException
from iconsdk.icon_service import IconService
from iconsdk.providers.async_provider import AsyncMonitor, AsyncProvider
from iconsdk.providers.provider import MonitorSpec
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils import get_timestamp
from iconsdk.utils.convert_type import convert_int_to_hex_str
from iconsdk.utils.validation import (is_block_height, is_hex_block_hash,
                                      is_predefined_block_value,
                                      is_score_address, is_T_HASH,
                                      is_wallet_address)


class AsyncIconService:
    """
    Async version of IconService using aiohttp for network requests.

    Handles asynchronous communication with an ICON node via JSON-RPC.
    """
    DEFAULT_BLOCK_VERSION = IconService.DEFAULT_BLOCK_VERSION # Use IconService's default

    def __init__(self, provider: AsyncProvider):
        self.__provider = provider

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.__provider.close()

    # --- Async API Methods ---

    async def call(self, call_obj: Call) -> Any:
        """Async version of IconService.call"""
        # Validation based on IconService.call
        if not isinstance(call_obj, Call):
            raise DataTypeException("Call object is unrecognized.")
        if not is_score_address(call_obj.to):
            raise AddressException(f"SCORE address is invalid: {call_obj.to}")
        if call_obj.from_ is not None and not is_wallet_address(call_obj.from_):
             raise AddressException(f"'from' address is invalid: {call_obj.from_}")

        req_params = {
            "to": call_obj.to,
            "dataType": "call",
            "data": {
                "method": call_obj.method,
                "params": call_obj.params or {} # Use empty dict if params is None
            }
        }
        if call_obj.from_ is not None:
            req_params["from"] = call_obj.from_
        if call_obj.height is not None:
            # IconService uses the height directly, assuming it's already hex or handled by provider
            # Here, we'll convert to hex for consistency with other methods
            req_params["height"] = hex(call_obj.height) if isinstance(call_obj.height, int) else call_obj.height

        result = await self.__provider.make_request('icx_call', req_params)
        # IconService doesn't convert the result for call, so we return raw
        return result # Return raw result, conversion handled by caller if needed

    async def get_balance(self, address: str, height: Optional[int] = None) -> int:
        """Async version of IconService.get_balance. Returns balance as integer."""
        # Validation from IconService.get_balance
        if not (is_score_address(address) or is_wallet_address(address)):
            raise AddressException(f"Address is invalid: {address}")

        # The result is typically hex string, convert it if needed by the caller
        # or adjust the return type hint if conversion happens here.
        # For now, returning the raw result from the node.
        req_params = {"address": address}
        if height is not None:
             req_params["height"] = hex(height) # Add height param if provided
        result = await self.__provider.make_request('icx_getBalance', req_params)
        # Mimic IconService conversion
        try:
            return int(result, 0)
        except (ValueError, TypeError):
             # Handle cases where result might not be a valid hex string
             raise DataTypeException(f"Failed to convert balance to integer: {result}")

    async def get_block(self, value: Union[str, int], block_version: str = DEFAULT_BLOCK_VERSION) -> Any:
        """Async version of IconService.get_block. Returns raw block data."""
        # Validation and logic adapted from IconService.get_block
        params: Optional[Dict[str, str]] = None
        prev_method: str = ""

        if is_block_height(value):
            params = {'height': hex(value)} # IconService uses hex here
            prev_method = 'icx_getBlockByHeight'
        elif is_hex_block_hash(value):
            params = {'hash': value}
            prev_method = 'icx_getBlockByHash'
        elif is_predefined_block_value(value): # Checks for "latest"
            params = None # No params for latest
            prev_method = 'icx_getLastBlock'
        else:
            raise DataTypeException(f"Invalid block reference: {value!r}. Use integer height, 'latest', or 0x-prefixed hash.")

        # Determine actual method based on block_version (mimicking IconService logic)
        method: str
        if block_version == self.DEFAULT_BLOCK_VERSION:
            method = prev_method
        else:
            # For newer block versions, IconService uses 'icx_getBlock'
            # and includes the identifier (height/hash) within the params.
            method = 'icx_getBlock'
            # If getting 'latest', params remain None for icx_getBlock
            # If getting by height/hash, the existing params dict is correct for icx_getBlock

        # Make the request
        result = await self.__provider.make_request(method, params) # Pass params dict directly

        # IconService does conversion if full_response is False. We skip async conversion for now.
        # Caller can handle conversion if needed.
        return result


    async def get_score_api(self, address: str, height: Optional[int] = None) -> Any:
        """Async version of IconService.get_score_api. Returns raw API list."""
        # Validation from IconService.get_score_api
        if not is_score_address(address):
            raise AddressException(f"SCORE Address is invalid: {address}")

        req_params = {"address": address}
        if height is not None:
             req_params["height"] = hex(height) # Add height param if provided
        result = await self.__provider.make_request('icx_getScoreApi', req_params)
        # IconService returns raw result here
        return result

    async def get_transaction(self, tx_hash: str) -> Any:
        """Async version of IconService.get_transaction. Returns raw transaction data."""
        # Validation from IconService.get_transaction
        if not is_T_HASH(tx_hash):
            raise DataTypeException(f"Transaction hash is invalid: {tx_hash}")

        # IconService.get_transaction uses 'icx_getTransactionByHash'
        result = await self.__provider.make_request('icx_getTransactionByHash', {"txHash": tx_hash})
        # IconService converts if full_response is False, skip async conversion
        return result

    async def get_transaction_result(self, tx_hash: str) -> Any:
        """Async version of IconService.get_transaction_result. Returns raw transaction result."""
        # Validation from IconService.get_transaction_result
        if not is_T_HASH(tx_hash):
            raise DataTypeException(f"Transaction hash is invalid: {tx_hash}")

        result = await self.__provider.make_request('icx_getTransactionResult', {"txHash": tx_hash})
        # IconService converts if full_response is False, skip async conversion
        return result

    # Add missing async version of get_score_status
    async def get_score_status(self, address: str, height: Optional[int] = None) -> Any:
        """Async version of IconService.get_score_status. Returns raw SCORE status."""
        # Validation from IconService.get_score_status
        if not is_score_address(address):
            raise AddressException(f"SCORE Address is invalid: {address}")

        req_params = {"address": address}
        if height is not None:
             req_params["height"] = hex(height) # Add height param if provided
        result = await self.__provider.make_request('icx_getScoreStatus', req_params)
        # IconService returns raw result here
        return result

    # Add missing async version of wait_transaction_result
    async def wait_transaction_result(self, tx_hash: str) -> Any:
        """Async version of IconService.wait_transaction_result. Returns raw transaction result."""
         # Validation from IconService.wait_transaction_result
        if not is_T_HASH(tx_hash):
            raise DataTypeException(f"Transaction hash is invalid: {tx_hash}")

        result = await self.__provider.make_request('icx_waitTransactionResult', {"txHash": tx_hash})
        # IconService converts if full_response is False, skip async conversion
        return result

    async def send_transaction(self, signed_transaction: SignedTransaction) -> Any:
        """Async version of IconService.send_transaction. Returns transaction hash."""
        if not isinstance(signed_transaction, SignedTransaction):
             raise DataTypeException("SignedTransaction object is unrecognized.")

        params = signed_transaction.signed_transaction_dict
        result = await self.__provider.make_request('icx_sendTransaction', params)
        # IconService returns raw tx_hash here
        return result

    # Add missing async version of send_transaction_and_wait
    async def send_transaction_and_wait(self, signed_transaction: SignedTransaction) -> Any:
        """Async version of IconService.send_transaction_and_wait. Returns raw transaction result."""
        if not isinstance(signed_transaction, SignedTransaction):
             raise DataTypeException("SignedTransaction object is unrecognized.")

        params = signed_transaction.signed_transaction_dict
        result = await self.__provider.make_request('icx_sendTransactionAndWait', params)
        # IconService converts if full_response is False, skip async conversion
        return result

    async def get_total_supply(self, height: Optional[int] = None) -> int:
        """Async version of IconService.get_total_supply. Returns total supply as integer."""
        req_params = {}
        if height is not None:
            req_params["height"] = hex(height) # IconService uses hex here
        # Pass params dict directly, or None if empty
        result = await self.__provider.make_request('icx_getTotalSupply', req_params if req_params else None)
        # Mimic IconService conversion
        try:
            return int(result, 16)
        except (ValueError, TypeError):
             raise DataTypeException(f"Failed to convert total supply to integer: {result}")

    # Add missing async version of estimate_step
    async def estimate_step(self, transaction: Transaction) -> int:
        """Async version of IconService.estimate_step. Returns step estimate as integer."""
        if not isinstance(transaction, Transaction):
            raise DataTypeException("Transaction object is unrecognized.")

        # Build params similar to IconService.estimate_step
        params = {
            "version": convert_int_to_hex_str(transaction.version) if transaction.version else "0x3",
            "from": transaction.from_,
            "to": transaction.to,
            "timestamp": convert_int_to_hex_str(transaction.timestamp) if transaction.timestamp else get_timestamp(),
            "nid": convert_int_to_hex_str(transaction.nid) if transaction.nid else "0x1"
        }

        if transaction.value is not None:
            params["value"] = convert_int_to_hex_str(transaction.value)
        if transaction.nonce is not None:
            params["nonce"] = convert_int_to_hex_str(transaction.nonce)
        if transaction.data_type is not None:
            params["dataType"] = transaction.data_type
        if transaction.data is not None:
            params["data"] = transaction.data

        result = await self.__provider.make_request('debug_estimateStep', params)
        # Mimic IconService conversion
        try:
            return int(result, 16)
        except (ValueError, TypeError):
             raise DataTypeException(f"Failed to convert step estimate to integer: {result}")


    # Add missing async version of get_trace
    async def get_trace(self, tx_hash: str) -> Any:
        """Async version of IconService.get_trace. Returns raw trace data."""
        # Validation from IconService.get_trace
        if not is_T_HASH(tx_hash):
            raise DataTypeException(f"Transaction hash is invalid: {tx_hash}")

        result = await self.__provider.make_request('debug_getTrace', {"txHash": tx_hash})
        # IconService returns raw result here
        return result

    # Add missing BTP/Data methods from IconService
    async def get_data_by_hash(self, _hash: str) -> Any:
        # IconService has no specific validation for _hash here
        """Async version of IconService.get_data_by_hash"""
        return await self.__provider.make_request('icx_getDataByHash', {'hash': _hash})

    async def get_block_header_by_height(self, height: int) -> Any:
        """Async version of IconService.get_block_header_by_height"""
        # Basic type check (IconService doesn't explicitly validate height here)
        if not isinstance(height, int) or height < 0:
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")
        return await self.__provider.make_request('icx_getBlockHeaderByHeight', {'height': hex(height)})

    async def get_votes_by_height(self, height: int) -> Any:
        """Async version of IconService.get_votes_by_height"""
         # Basic type check (IconService doesn't explicitly validate height here)
        if not isinstance(height, int) or height < 0:
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")
        return await self.__provider.make_request('icx_getVotesByHeight', {'height': hex(height)})

    async def get_proof_for_result(self, _hash: str, index: int) -> Any:
        """Async version of IconService.get_proof_for_result"""
        # Basic validation (IconService doesn't explicitly validate here)
        if not is_T_HASH(_hash): # Assuming block hash format
             raise DataTypeException(f"Hash is invalid: {_hash}")
        if not isinstance(index, int) or index < 0:
            raise DataTypeException(f"Index must be a non-negative integer: {index}")

        params = {'hash': _hash, 'index': hex(index)}
        return await self.__provider.make_request('icx_getProofForResult', params)

    async def get_proof_for_events(self, _hash: str, index: int, events: List[str] = []) -> Any:
        """Async version of IconService.get_proof_for_events"""
         # Basic validation (IconService doesn't explicitly validate here)
        if not is_T_HASH(_hash): # Assuming block hash format
             raise DataTypeException(f"Hash is invalid: {_hash}")
        if not isinstance(index, int) or index < 0:
            raise DataTypeException(f"Index must be a non-negative integer: {index}")
        # IconService expects list of hex strings for events, but accepts empty list.
        # No strict validation on event format here, assuming caller provides correct format.
        if not isinstance(events, list): # Basic type check
             raise DataTypeException(f"Events must be a list: {events}")

        # Pass events directly as IconService expects List[str] (likely hex strings)
        params = {'hash': _hash, 'index': hex(index), 'events': events}
        return await self.__provider.make_request('icx_getProofForEvents', params)

    async def get_btp_network_info(self, id: int, height: Optional[int] = None) -> Any:
        """Async version of IconService.get_btp_network_info"""
        # Basic type check (IconService doesn't explicitly validate here)
        if not isinstance(id, int):
             raise DataTypeException(f"BTP Network ID must be an integer: {id}")
        if height is not None and (not isinstance(height, int) or height < 0):
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")

        params = {'id': hex(id)}
        if height is not None:
            params['height'] = hex(height)
        return await self.__provider.make_request('btp_getNetworkInfo', params)

    async def get_btp_network_type_info(self, id: int, height: Optional[int] = None) -> Any:
        """Async version of IconService.get_btp_network_type_info"""
        # Basic type check (IconService doesn't explicitly validate here)
        if not isinstance(id, int):
             raise DataTypeException(f"BTP Network Type ID must be an integer: {id}")
        if height is not None and (not isinstance(height, int) or height < 0):
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")

        params = {'id': hex(id)}
        if height is not None:
            params['height'] = hex(height)
        return await self.__provider.make_request('btp_getNetworkTypeInfo', params)

    async def get_btp_messages(self, height: int, network_id: int) -> Any:
        """Async version of IconService.get_btp_messages"""
        # Basic type check (IconService doesn't explicitly validate here)
        if not isinstance(height, int) or height < 0:
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")
        if not isinstance(network_id, int):
             raise DataTypeException(f"BTP Network ID must be an integer: {network_id}")

        params = {'height': hex(height), 'networkID': hex(network_id)}
        return await self.__provider.make_request('btp_getMessages', params)

    async def get_btp_header(self, height: int, network_id: int) -> Any:
        """Async version of IconService.get_btp_header"""
        # Basic type check (IconService doesn't explicitly validate here)
        if not isinstance(height, int) or height < 0:
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")
        if not isinstance(network_id, int):
             raise DataTypeException(f"BTP Network ID must be an integer: {network_id}")

        params = {'height': hex(height), 'networkID': hex(network_id)}
        return await self.__provider.make_request('btp_getHeader', params)

    async def get_btp_proof(self, height: int, network_id: int) -> Any:
        """Async version of IconService.get_btp_proof"""
        # Basic type check (IconService doesn't explicitly validate here)
        if not isinstance(height, int) or height < 0:
            raise DataTypeException(f"Block height must be a non-negative integer: {height}")
        if not isinstance(network_id, int):
             raise DataTypeException(f"BTP Network ID must be an integer: {network_id}")

        params = {'height': hex(height), 'networkID': hex(network_id)}
        return await self.__provider.make_request('btp_getProof', params)

    async def get_btp_source_information(self) -> Any:
        """Async version of IconService.get_btp_source_information"""
        return await self.__provider.make_request('btp_getSourceInformation') # No params

    async def get_network_info(self) -> Any:
         """Async version of IconService.get_network_info"""
         return await self.__provider.make_request('icx_getNetworkInfo')


    async def monitor(self, spec: MonitorSpec, keep_alive: Optional[float] = None) -> AsyncMonitor:
        return await self.__provider.make_monitor(spec, keep_alive)
    
__all__ = ['AsyncIconService']