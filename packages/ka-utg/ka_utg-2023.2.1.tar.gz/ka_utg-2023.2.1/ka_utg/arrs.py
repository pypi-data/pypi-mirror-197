# coding=utf-8

from typing import Dict, List


class Arrs:
    """
    Manage Arrays
    """
    @staticmethod
    def sh_dic(keys: List, values: List) -> None | Dict:
        if keys is None or keys == []:
            return None
        return dict(zip(keys, values))

    @staticmethod
    def ex_intersection(
            arr0: None | List, arr1: None | List) -> None | List:
        if arr0 is None:
            return None
        if arr1 is None:
            return None
        return list(set(arr0).intersection(set(arr1)))
