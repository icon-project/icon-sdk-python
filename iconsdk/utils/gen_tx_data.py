from typing import Optional

from ..exception import DataTypeException
from ..utils.typing.conversion import object_to_str

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
            "content": transaction.content
        }
        # Params is an optional property.
        if transaction.params:
            data["params"] = transaction.params
    elif transaction.data_type == "call":
        data = {"method": transaction.method}
        # Params is an optional property.
        if transaction.params:
            data["params"] = object_to_str(transaction.params)
    else:
        raise DataTypeException(f"Invalid dataType: {transaction.data_type}")

    return object_to_str(data)
