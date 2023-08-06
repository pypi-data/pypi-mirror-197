import warnings
from typing import TypeVar


def deprecation_message(method: str, deprecated_in: str, removed_in: str, details: str) -> str:
    """
    Generates a deprecation message for deprecation a function.

    This call:
        warnings.warn(deprecation_message("foo", "1.0.0", "1.1.0", "reason), category=DeprecationWarning)

    Will result in:
        "foo is deprecated since "1.0.0" and will be removed in "1.1.1. reason"

    :param method: The name of the deprecated method.

    :param deprecated_in: The version at which the method is considered deprecated.
                          This will usually be the next version to be released when the warning is added.

    :param removed_in: The version when the method will be removed.

    :param details: Extra details to be added to the method docstring and warning.
                    For example, the details may point users to a replacement method, such as "Use the foo_bar method instead"
    """
    return f'{method} is deprecated since "{deprecated_in}" and will be removed in "{removed_in}". {details}'


ValueType = TypeVar("ValueType")


def deprecate_to_property(value: ValueType, name: str, deprecated_in: str, removed_in: str, details: str) -> ValueType:
    value_type = type(value)

    class DeprecatedProperty(value_type):
        def __call__(self, *args, **kwargs):
            warnings.warn(deprecation_message(name, deprecated_in, removed_in, details), category=DeprecationWarning)
            return value_type(self)

    return DeprecatedProperty(value)
