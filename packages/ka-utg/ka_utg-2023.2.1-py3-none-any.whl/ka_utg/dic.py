# coding=utf-8

from ka_com.log import Log
from ka_utg.arr import Arr
from ka_utg.obj import Obj

from typing import Any, Dict, Generator, List, Tuple

T_DoA = Dict[Any, List[Any]]


class Dic:
    """
    Manage Dictionary
    """
    @staticmethod
    def copy(
            dic_target: None | Dict[Any, Any],
            dic_source: None | Dict[Any, Any],
            keys: None | List[Any] = None) -> None:
        if dic_target is None:
            return
        if dic_source is None:
            return
        if keys is None:
            keys = list(dic_source.keys())
        for key in keys:
            dic_target[key] = dic_source[key]

    @classmethod
    def append(
            cls, dic: Dict[Any, Any],
            keys: List[Any],
            value: Any,
            item0: Any = None) -> None:
        if item0 is None:
            item0 = []
        if dic is None or keys is None or value is None:
            return
        if not isinstance(keys, (list, tuple)):
            keys = [keys]
        cls.set(dic, keys, item0)
        dic[keys[-1]].append(value)

    @classmethod
    def extend(
            cls, dic: Dict[Any, Any], keys: List[Any],
            arr: List[Any], item0=None) -> None:
        if item0 is None:
            item0 = []
        if dic is None or keys is None or arr is None:
            return
        if not isinstance(keys, (list, tuple)):
            keys = [keys]
        cls.set(dic, keys, item0)
        dic[keys[-1]].extend(arr)

    @classmethod
    def new(cls, keys, value) -> None | Dict[Any, Any]:
        if keys is None or value is None:
            return None
        dic: Dict[Any, Any] = {}
        cls.set(dic, keys, value)
        return dic

    @staticmethod
    def set(dic, keys, value) -> None:
        if dic is None or keys is None or value is None:
            return
        if not isinstance(keys, (list, tuple)):
            dic[keys] = value
            return
        _dic = dic
        # all element except the last one
        for key in keys[:-1]:
            if key not in _dic:
                _dic[key] = {}
            _dic = _dic[key]
        # last element
        _dic[keys[-1]] = value

    @staticmethod
    def increment(
            dic: None | Dict[Any, Any],
            keys: None | List[Any] | Tuple[Any],
            item0: Any = 1) -> None:
        if dic is None:
            return
        if keys is None:
            return

        if not isinstance(keys, (list, tuple)):
            keys = [keys]

        dic_ = dic

        # all element except the last one
        for key in keys[:-1]:
            if key not in dic_:
                dic_[key] = {}
            dic_ = dic_[key]

        # last element
        key = keys[-1]

        if key not in dic_:
            dic_[key] = item0
        else:
            dic_[key] += 1

    @staticmethod
    def lstrip_keys(
            dic: Dict[Any, Any], str: str) -> Dict[Any, Any]:
        dic_new: Dict[Any, Any] = {}
        for k, v in dic.items():
            k_new = k.replace(str, "", 1)
            dic_new[k_new] = v
        return dic_new

    @staticmethod
    def is_not(
            dic: Dict[Any, Any], key: str) -> None | bool:
        if key in dic:
            return not dic[key]
        else:
            return None

    @staticmethod
    def nvl(
            dic: None | Dict[Any, Any]) -> Dict[Any, Any]:
        """ nvl function similar to SQL NVL function
        """
        if dic is None:
            return {}
        return dic

    @staticmethod
    def sh_prefixed(
            dic: Dict[Any, Any], prefix: str) -> Dict[Any, Any]:
        dic_new: Dict[Any, Any] = {}
        for key, value in dic.items():
            dic_new[f"{prefix}_{key}"] = value
        return dic_new

    @staticmethod
    def sh_value2keys(
            dic: Dict[Any, Any]) -> Dict[Any, Any]:
        dic_new: Dict[Any, Any] = {}
        for key, value in dic.items():
            if value not in dic_new:
                dic_new[value] = []
            if key not in dic_new[value]:
                dic_new[value].extend(key)
        return dic_new

    class Names:

        @staticmethod
        def sh(
                d_data: Dict[Any, Any],
                key: str = 'value') -> Any:
            try:
                return Obj.extract_values(d_data, key)
            except Exception as e:
                Log.error(e, exc_info=True)
                return []

        @classmethod
        def sh_item0(
                cls, d_names: Dict[Any, Any]) -> Any:
            names = cls.sh(d_names)
            return Arr.sh_item0(names)

        @classmethod
        def sh_item0_if(
                cls, string: str,
                d_names: Dict[Any, Any]) -> Any:
            names = cls.sh(d_names)
            return Arr.sh_item0_if(string, names)

    class Key:

        @staticmethod
        def change(
                dic: Dict[Any, Any],
                source_key: Dict[Any, Any],
                target_key: Dict[Any, Any]) -> Dict[Any, Any]:
            if source_key in dic:
                dic[target_key] = dic.pop(source_key)
            return dic

    class Value:

        @staticmethod
        def get(dic, keys, default=None):
            if keys is None:
                return dic
            if len(keys) == 0:
                return dic

            value = dic
            for key in keys:
                if key not in value:
                    return default
                value = value[key]
                if value is None:
                    break
            return value

        @classmethod
        def set(
                cls, dic: None | Dict[Any, Any],
                keys: None | List[Any] | Tuple[Any],
                value: Any) -> None:
            if value is None:
                return
            if dic is None:
                return
            if keys is None:
                return

            if not isinstance(keys, (list, tuple)):
                keys = [keys]

            value_curr = cls.get(dic, keys[:-1])
            if value_curr is None:
                return
            last_key = keys[-1]
            if last_key in value_curr:
                value_curr[last_key] = value

        @classmethod
        def is_empty(
                cls, dic: None | Dict[Any, Any],
                keys: List[Any] | Tuple[Any]) -> bool:
            if dic is None:
                return True
            if isinstance(keys, str):
                keys = [keys]
            if isinstance(keys, (list, tuple)):
                value_curr = cls.get(dic, keys)
                if value_curr is None:
                    return True
                if isinstance(value_curr, str):
                    if value_curr == '':
                        return True
                elif isinstance(value_curr, (list, tuple)):
                    if value_curr == []:
                        return True
                elif isinstance(value_curr, dict):
                    if value_curr == {}:
                        return True
            return False

        @classmethod
        def is_not_empty(
                cls, dic: None | Dict[Any, Any],
                keys: List[Any] | Tuple[Any]) -> bool:
            return not cls.is_empty(dic, keys)

    @staticmethod
    def change_keys_with_keyfilter(
            dic: Dict[Any, Any],
            keyfilter: Dict[Any, Any]) -> Dict[Any, Any]:
        dic_new: Dict[Any, Any] = {}
        for key, value in dic.items():
            key_new = keyfilter.get(key)
            if key_new is None:
                continue
            dic_new[key_new] = value
        return dic_new

    @staticmethod
    def yield_values_with_keyfilter(
            dic: Dict[Any, Any],
            keyfilter: Dict[Any, Any]) -> Generator:
        for key, value in dic.items():
            if key in keyfilter:
                yield value

    @staticmethod
    # def get_value_for_keys(
    def get(
            dic: Dict[Any, Any], keys: List[Any] | Tuple[Any]) -> None | Any:
        _dic = dic
        value = None
        for _key in keys:
            value = _dic.get(_key)
            if value is None:
                return None
            if not isinstance(value, dict):
                return value
            _dic = value
        return value
