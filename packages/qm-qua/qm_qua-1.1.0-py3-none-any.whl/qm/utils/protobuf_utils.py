import dataclasses
import logging
from typing import Union, Dict, Iterable

import betterproto

from qm.grpc.general_messages import MessageLevel

LOG_LEVEL_MAP = {
    MessageLevel.Message_LEVEL_ERROR: logging.ERROR,
    MessageLevel.Message_LEVEL_WARNING: logging.WARN,
    MessageLevel.Message_LEVEL_INFO: logging.INFO,
}


def list_fields(node) -> Dict[str, Union[betterproto.Message, Iterable]]:
    fields = dataclasses.fields(node)
    output = {}
    for field in fields:
        field_value = getattr(node, field.name)
        if isinstance(field_value, Iterable) or (
            isinstance(field_value, betterproto.Message) and betterproto.serialized_on_wire(field_value)
        ):
            output[field.name] = field_value
    return output
