# coding=utf-8

from datetime import datetime
# import pendulum

from typing import Any

from ka_com.com import Com
from ka_utg.log import Log
from ka_utg.dic import Dic


class Timestamp:

    @staticmethod
    def sh_elapse_time_sec(
            end: Any,
            start: None | Any) -> None | Any:
        if start is None:
            return None
        return end.timestamp()-start.timestamp()


class Timer:
    """ Timer Management
    """
    @staticmethod
    def start(package: str, module: None | str) -> None:
        """ start Timer
        """
        if Com.d_timer is None:
            Com.d_timer = {}
        if package not in Com.d_timer:
            Com.d_timer[package] = {}
        if module is not None:
            keys = [package, module, "start"]
        else:
            keys = [package, "start"]
        Dic.set(Com.d_timer, keys, datetime.now())
        # Dic.set(Com.d_timer, keys, pendulum.now())

    @staticmethod
    def end(package: str, module: None | str) -> None:
        """ end Timer
        """
        if module is not None:
            keys = [package, module, "start"]
            msg = f"{package}.{module}"
        else:
            keys = [package, "start"]
            msg = package

        start = Dic.get(Com.d_timer, keys)
        end = datetime.now()
        # end = pendulum.now()
        # elapse_time = end-start
        elapse_time_sec = Timestamp.sh_elapse_time_sec(end, start)
        # elapse_time_sec = end.diff(start).in_words()
        msg = f"{msg} elapse time [sec] = {elapse_time_sec}"

        Log.info(msg, stacklevel=2)
