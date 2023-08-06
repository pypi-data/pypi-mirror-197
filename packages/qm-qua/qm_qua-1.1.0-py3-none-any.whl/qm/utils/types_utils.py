from typing import TypeVar, Collection, Type

import numpy as np

T = TypeVar("T")


def fix_object_data_type(obj: T) -> T:
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        obj_item = obj.item()
        if type(obj_item) is np.longdouble:
            return float(obj_item)
        else:
            return obj_item
    else:
        return obj


def get_all_iterable_data_types(it):
    return set([type(e) for e in it])


def collection_has_type(collection: Collection, type_to_check: Type, include_subclasses: bool) -> bool:
    if include_subclasses:
        return any([isinstance(i, type_to_check) for i in collection])
    else:
        return any([type(i) is type_to_check for i in collection])


def collection_has_type_bool(collection: Collection):
    return collection_has_type(collection, bool, False) or collection_has_type(collection, np.bool_, True)


def collection_has_type_int(collection: Collection):
    return collection_has_type(collection, int, False) or collection_has_type(collection, np.integer, True)


def collection_has_type_float(collection: Collection):
    return collection_has_type(collection, float, False) or collection_has_type(collection, np.floating, True)


def is_iter(x):
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True


def get_iterable_elements_datatype(it):
    if isinstance(it, np.ndarray):
        return type(it[0].item())
    elif is_iter(it):
        if len(get_all_iterable_data_types(it)) > 1:
            raise ValueError("Multiple datatypes encountered in iterable object")
        if isinstance(it[0], np.generic):
            return type(it[0].item())
        else:
            return type(it[0])
    else:
        return None
