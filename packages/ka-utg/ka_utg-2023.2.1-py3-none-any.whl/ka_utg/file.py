# coding=utf-8
import glob
import os

from ka_utg.log import Log


class File:

    class Latest:

        @staticmethod
        def get(path_pattern):
            """
            get latest path that match path pattern
            """
            return File.get_latest(path_pattern)

    @staticmethod
    def io(obj, path, io_function):
        """
        execute io function
        """
        io_function(obj, path)

    @staticmethod
    def get_paths(path_pattern, recursive=False):
        """
        get all paths that match path_pattern
        """
        _paths = glob.iglob(path_pattern, recursive=recursive)
        print(f"file.get_paths path_pattern = {path_pattern}")
        print(f"file.get_paths _paths = {_paths}")
        for _path in _paths:
            if os.path.isfile(_path):
                print(f"file.get_paths _path = {_path}")
                yield _path

    @staticmethod
    def get_latest(path_pattern):
        """
        get latest path that match path pattern
        """
        iter_path = glob.iglob(path_pattern)
        a_path = list(iter_path)
        if len(a_path) > 0:
            return max(a_path, key=os.path.getmtime)
        msg = f"No path exist for pattern: {path_pattern}"
        Log.error(msg)
        return None

    @staticmethod
    def count(path_pattern):
        """
        count number of paths that match path pattern
        """
        return len(list(glob.iglob(path_pattern)))
