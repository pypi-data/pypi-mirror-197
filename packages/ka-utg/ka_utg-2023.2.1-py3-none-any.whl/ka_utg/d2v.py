# coding=utf-8

from typing import Any, Dict, Generator, List


class D2V:
    @classmethod
    def sh_union(cls, d2_arr: Dict) -> List:
        arr_new = []
        for _key1, _key2, arr in cls.yield_values(d2_arr):
            arr_new.extend(arr)
        return arr_new

    @staticmethod
    def append(d2_v: Dict, keys: List, value) -> Dict:
        key0 = keys[0]
        key1 = keys[1]
        if key0 not in d2_v:
            d2_v[key0] = {}
        if key1 not in d2_v[key0]:
            d2_v[key0][key1] = []
        d2_v[key0][key1].append(value)
        return d2_v

    @staticmethod
    def set(d2_v: Dict, keys: List, value: Any) -> Dict:
        key0 = keys[0]
        key1 = keys[1]
        if key0 not in d2_v:
            d2_v[key0] = {}
        d2_v[key0][key1] = value
        return d2_v

    @staticmethod
    def sh_key2values(d2_v: Dict) -> Dict:
        dic: Dict = {}
        for key1, d_v in d2_v.items():
            if key1 not in dic[key1]:
                dic[key1] = {}
            for key2, _dummy in d_v.items():
                dic[key1].append(key2)

        return d2_v

    @staticmethod
    def yield_values(d2_v: Dict) -> Generator:
        for key1, d_v in d2_v.items():
            for key2, value in d_v.items():
                yield (key1, key2, value)
