# coding=utf-8

from typing import Any, Dict, List


class DoD:
    """ Manage Dictionary of Dictionaries
    """
    @staticmethod
    def sh_value(
            dic: None | Dict, keys: None | str | List) -> None | Any:
        if dic is None or keys is None or keys == []:
            return None
        if not isinstance(dic, dict):
            return None
        if isinstance(keys, str):
            keys = [keys]

        _dic = dic
        for key in keys:
            value = _dic.get(key)
            if value is None:
                return value
            if not isinstance(value, dict):
                return value
            _dic = value
        return value

    @staticmethod
    def nvl(dod: None | Dict) -> None | Dict:
        """ nvl function similar to SQL NVL function
        """
        if dod is None:
            return {}
        return dod

    @classmethod
    def replace_keys(cls, dic: Dict, keys: Dict) -> Dict:
        """ recurse through the dictionary while building a new one
            with new keys from a keys dictionary
        """
        dic_new = {}
        for key in dic.keys():
            key_new = keys.get(key, key)
            if isinstance(dic[key], dict):
                dic_new[key_new] = cls.replace_keys(dic[key], keys)
            else:
                dic_new[key_new] = dic[key]
        return dic_new
