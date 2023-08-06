# coding=utf-8

import os
import re

from ka_utg.log import Log


class Ver:
    """ Manage Verifcation
    """
    msg_path = "Given path: {zpath} has a wrong format or not existing"
    msg_email = "Wrong email address: {email}"
    msg_module = "Given module: {module} is not defined"

    @staticmethod
    def is_none(obj):
        return True if obj is None else False

    @staticmethod
    def is_not_none(obj):
        return False if obj is None else True

    @classmethod
    def path(cls, zpath):
        if os.path.exists(zpath):
            return True
        Log.error(cls.msg_path.formst(zpath))
        return False

    @classmethod
    def email(cls, email):
        match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
        if match:
            return True
        Log.error(cls.msg_email.format(email))
        return False

    @staticmethod
    def name(name):
        if len(name) > 1:
            return True
        return False

    @classmethod
    def module(cls, module, a_module):
        if module in a_module:
            return True
        Log.error(cls.msg_module.format(module))
        return False
