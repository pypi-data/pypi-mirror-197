#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      register
   Description:
   Author:          dingyong.cui
   date：           2023/3/15
-------------------------------------------------
   Change Activity:
                    2023/3/15
-------------------------------------------------
"""
import importlib
import inspect
import logging
import pkgutil
from typing import List

logger = logging.getLogger(__name__)

_DEFAULT_RELATE_NAME = 'service'


class Register:

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__()
        self._dict = {}

    def register(self, target):
        def add_register_item(key, value):
            if not callable(value):
                raise Exception(f"register object must be callable! But receive:{value} is not callable!")
            if key in self._dict:
                logger.warning(f"{value.__name__} has been registered before, so we will overriden it")
            self._dict[key] = value

            return value

        if callable(target):  # 如果传入的目标可调用，说明之前没有给出注册名字，我们就以传入的函数或者类的名字作为注册名
            return add_register_item(target.__name__, target)

        return lambda x: add_register_item(target, x)

    def __call__(self, target):
        return self.register(target)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()


aps_register = Register()


def autodiscover_aps(relate_name=None) -> List:
    aps_funcs = []
    if relate_name is None:
        relate_name = _DEFAULT_RELATE_NAME

    from django.apps import apps
    for app_config in apps.get_app_configs():
        pkg = app_config.module
        pkg_path = f'{pkg.__path__[0]}\\{relate_name}'
        pkg_name = f'{pkg.__name__}.{relate_name}'
        part_aps_funcs = _autodiscover_aps(pkg_path, pkg_name)
        aps_funcs.extend(part_aps_funcs)

    return aps_funcs


def _autodiscover_aps(pkg_path, pkg_name):
    part_aps_funcs = []
    for _, file, is_pkg in pkgutil.iter_modules([pkg_path]):
        py_module = importlib.import_module(f'.{file}', package=pkg_name)
        for name, p_cls in inspect.getmembers(py_module):
            if isinstance(p_cls, Register):
                for func in p_cls.items():
                    aps_func = _convert_func(func)
                    part_aps_funcs.append(aps_func)

    return part_aps_funcs


def _convert_func(func: tuple):
    func = func[1]
    func_module = func.__module__
    func_name = func.__qualname__
    func_params = inspect.getfullargspec(func).args
    func_params = [fp for fp in func_params if fp != 'self']

    aps_func = {
        'func_module': func_module,
        'func': func_name,
        'func_params': func_params
    }

    return aps_func
