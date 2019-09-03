from typing import Optional

from iconsdk.utils.convert_type import convert_params_value_to_hex_str
from iconsdk.utils.hexadecimal import add_0x_prefix

"""Generator for transaction data"""


def generate_data_value(transaction) -> Optional[dict]:
    """
    Generates data value in transaction from the other data like content_type, content, method or params
    by data types such as deploy and call.
    """
    if transaction.data_type == "deploy":
        # Content's data type is bytes and return value is hex string prefixed with '0x'.
        data = {
            "contentType": transaction.content_type,
            "content": add_0x_prefix(transaction.content.hex())
        }
        # Params is an optional property.
        if transaction.params:
            data["params"] = convert_params_value_to_hex_str(transaction.params)
    elif transaction.data_type == "call":
        data = {"method": transaction.method}
        # Params is an optional property.
        if transaction.params:
            data["params"] = convert_params_value_to_hex_str(transaction.params)
    return data
