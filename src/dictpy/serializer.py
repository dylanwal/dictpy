"""
This class is useful for turning custom python classes into JSON compatible dictionaries.
"""

from typing import Dict
from abc import ABC


VALID_TYPES = (str, float, int, bool)


class Serializer(ABC):
    """Base abstract class for a serializer object."""

    def to_JSON(self, remove_none: bool = True, skip: set[str] = None) -> dict:
        if remove_none:
            return self.remove_none(self.dict_cleanup(self.as_dict(skip)))

        return self.dict_cleanup(self.as_dict(skip))

    def as_dict(self, skip: set[str] = None) -> dict:
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        if skip:
            keys = {k for k in keys if k not in skip}

        attr = dict()
        for k in keys:
            value = self._to_dict(self.__getattribute__(k))
            attr[k] = value

        return attr

    @staticmethod
    def _to_dict(obj):
        """Convert obj to a dictionary, and return it."""
        if isinstance(obj, list):
            return [Serializer._to_dict(i) for i in obj]
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        else:
            return obj

    @staticmethod
    def remove_none(ddict: Dict) -> Dict:
        """Remove 'key, value' pair form dictionary if value is None or []."""
        _dict = {}
        for k, v in ddict.items():
            if v is None or v == []:
                continue
            elif isinstance(v, dict):
                _dict[k] = Serializer.remove_none(v)
            elif isinstance(v, list):
                _list = []
                for obj in v:
                    if isinstance(obj, dict):
                        obj = Serializer.remove_none(obj)
                    _list.append(obj)
                _dict[k] = _list
            else:
                _dict[k] = v

        return _dict

    @staticmethod
    def dict_cleanup(_dict: Dict) -> Dict:
        """Converts any non-JSON covertable objects to strings."""
        attr = dict()
        for k, v in _dict.items():
            value = Serializer._loop_through(v)
            attr[k] = value

        return attr

    @staticmethod
    def _loop_through(obj):
        """Loops through coverting everthing invalid into a string."""
        if isinstance(obj, list):
            return [Serializer._loop_through(i) for i in obj]
        elif isinstance(obj, dict):
            return Serializer.dict_cleanup(obj)
        elif isinstance(obj, VALID_TYPES) or obj is None:
            return obj
        else:
            return str(obj)
