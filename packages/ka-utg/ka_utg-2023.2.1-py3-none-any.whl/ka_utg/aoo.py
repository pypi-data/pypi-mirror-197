# coding=utf-8

from typing import List


class AoO:
    """ Manage Array of Objects
    """
    @staticmethod
    def to_unique(aoo: List):
        """ Removes duplicates from Array of Objects
        """
        aoo_new = []
        for ee in aoo:
            if ee not in aoo_new and ee is not None:
                aoo_new.append(ee)
        return aoo_new
