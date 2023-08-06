# coding=utf-8

# from ka_utg.log import Log
from ka_utg.arr import Arr

from typing import Any, Dict, List

T_AoA = List[List[Any]]
T_AoD = List[Dict[Any, Any]]


class AoA:
    """ Manage Array of Arrays
    """
    @staticmethod
    def nvl(aoa: T_AoA) -> T_AoA:
        """ nvl function similar to SQL NVL function
        """
        if aoa is None:
            return []
        return aoa

    @staticmethod
    def to_aod(
            aoa: T_AoA, keys: List[Any]) -> T_AoD:
        """ Migrate Array of Arrays to Array of Dictionaries
        """
        aod: T_AoD = []
        for _arr in aoa:
            dic = Arr.to_dic(_arr, keys)
            aod.append(dic)
        return aod
