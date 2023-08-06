# coding=utf-8

from ka_utg.arr import Arr
from ka_utg.dic import Dic

from typing import Dict, List, Tuple, Any

T_DoA = Dict[Any, List[Any]]

# T_Arr = NewType('T_Arr', Union[List[Any], Tuple[Any]])
# T_DoDA = NewType('T_DoDA', Dict[T_DA])
# T_DA = NewType('T_DA', Union[Dict, T_Arr])
# T_SLT = NewType('T_SLT', Union[str, List, Tuple])
# T_SLTD = NewType('T_SLTD', Union[str, List, Tuple, Dict])


class DoA:
    """
    Manage Dictionary of Array
    """
    @staticmethod
    def apply(
            arr_function,
            doa: Dict[Any, Any],
            keys: List[Any], item,
            item0: None | Any) -> None:
        """
        assign item to dictionary defined as value
        for the given keys.
        """
        if item0 is None:
            item0 = []
        if isinstance(keys, str):
            keys = [keys]
        elif not isinstance(keys, (list, tuple)):
            return

        _doa = doa
        # all elements of keys except the last
        for key in keys[:-1]:
            if key not in _doa:
                _doa[key] = []
            _doa = _doa[key]

        # last element of keys
        key = keys[-1]
        Dic.set(_doa, key, item0)
        _doa[key].append(item)
        arr_function(_doa[key], item)

    @staticmethod
    def append(
            doa: Dict[Any, Any],
            keys: List[Any] | Tuple[Any],
            item: None | Any,
            item0: None | Any = None) -> None:
        """
        assign item to dictionary defined as value
        for the given keys.
        """
        if item0 is None:
            item0 = []
        if isinstance(keys, str):
            keys = [keys]
        elif not isinstance(keys, (list, tuple)):
            return

        _doa = doa
        # all keys elements except the last
        for key in keys[:-1]:
            if key not in _doa:
                _doa[key] = {}
            _doa = _doa[key]

        # last keys element
        key = keys[-1]
        if key not in _doa:
            _doa[key] = item0
        _doa[key].append(item)

    @staticmethod
    def append_unique(
            doa: Dict[Any, Any],
            keys: List[Any] | Tuple[Any],
            item: Any,
            item0: None | Any = None) -> None:
        """
        assign item to dictionary defined as value
        for the given keys.
        """
        if item0 is None:
            item0 = []
        if isinstance(keys, str):
            keys = [keys]
        elif not isinstance(keys, (list, tuple)):
            return

        _doa = doa
        # all keys elements except the last
        for key in keys[:-1]:
            if key not in _doa:
                _doa[key] = {}
            _doa = _doa[key]

        # last keys element
        key = keys[-1]
        if key not in _doa:
            _doa[key] = item0
        Arr.append_unique(_doa[key], item)

    @staticmethod
    def extend(
            doa: Dict[Any, Any],
            keys: List[Any] | Tuple[Any],
            item: Any) -> None:
        """
        assign item to dictionary defined as value
        for the given keys.
        """
        if isinstance(keys, str):
            keys = [keys]
        if not isinstance(keys, (list, tuple)):
            return
        _doa = doa

        # all keys elements except the last
        for key in keys[:-1]:
            if key not in _doa:
                _doa[key] = {}
            _doa = _doa[key]

        # last keys element
        key = keys[-1]
        if isinstance(item, str):
            item = [item]
        if key not in _doa:
            _doa[key] = item
        else:
            _doa[key].extend(item)

    @staticmethod
    def set(
            doa: Dict[Any, Any],
            keys: List[Any] | Tuple[Any],
            item0: None | Any = None) -> None:
        """
        assign item to dictionary defined as value
        for the given keys.
        """
        if item0 is None:
            item0 = []
        if isinstance(keys, str):
            keys = [keys]
        elif not isinstance(keys, (list, tuple)):
            return
        _doa = doa

        # all keys elements except the last
        for key in keys[:-1]:
            if key not in _doa:
                _doa[key] = {}
            _doa = _doa[key]

        # last keys element
        key = keys[-1]
        if key not in _doa:
            _doa[key] = item0

    @staticmethod
    def sh_union(
            doa: T_DoA) -> List[Any]:
        arr_new = []
        for _key, _arr in doa.items():
            arr_new.extend(_arr)
        return arr_new
