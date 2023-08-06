from typing import TypeVar, Type, Any

T = TypeVar("T")


class Singleton(type):
    _instances = {}

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def delete_instances_for_type(mcs, type_to_delete: Type[T]) -> None:
        if type_to_delete in mcs._instances:
            mcs._instances.pop(type_to_delete)
