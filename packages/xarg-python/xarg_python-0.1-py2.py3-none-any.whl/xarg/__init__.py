#!/usr/bin/python3
# coding:utf-8
# Copyright (c) 2023 ZouMingzhe <zoumingzhe@qq.com>

__version__ = "0.1"

import argparse


class xarg():
    '''
    '''

    def __init__(self, prog=None, **kwargs):
        kwargs.update({"prog": prog})
        self.__xarg = argparse.ArgumentParser(**kwargs)

    @staticmethod
    def check_name_opt(fn):
        '''
        check option argument name
        '''

        def make_decorater(self, *name, **kwargs):
            for n in name:
                assert type(n) is str
                assert n[0] == '-'
            return fn(self, *name, **kwargs)

        return make_decorater

    @staticmethod
    def check_name_pos(fn):
        '''
        check position argument name
        '''

        def make_decorater(self, name, *args, **kwargs):
            assert type(name) is str
            assert name[0] != '-'
            return fn(self, name, *args, **kwargs)

        return make_decorater

    @check_name_opt
    def add_opt(self, *name, **kwargs):
        '''
        '''
        self.__xarg.add_argument(*name, **kwargs)

    @check_name_opt
    def add_opt_on(self, *name, **kwargs):
        '''
        boolean option argument, default value is False
        '''
        kwargs.update({
            "action": 'store_true',
        })
        for key in ("type", "nargs", "const", "default", "choices"):
            if key in kwargs:
                kwargs.pop(key)
        self.__xarg.add_argument(*name, **kwargs)

    @check_name_opt
    def add_opt_off(self, *name, **kwargs):
        '''
        boolean option argument, default value is True
        '''
        kwargs.update({
            "action": 'store_false',
        })
        for key in ("type", "nargs", "const", "default", "choices"):
            if key in kwargs:
                kwargs.pop(key)
        self.__xarg.add_argument(*name, **kwargs)

    @check_name_pos
    def add_pos(self, name, nargs=0, **kwargs):
        '''
        nargs < 0: at least 1
        nargs = 0: 0 or 1
        nargs > 0: n
        default type is str
        '''
        assert type(nargs) is int
        kwargs.update({
            "nargs": nargs if nargs > 0 else "+" if nargs else "?",
        })
        self.__xarg.add_argument(name, **kwargs)

    def parse_args(self) -> argparse.Namespace:
        '''
        '''
        args = self.__xarg.parse_args()
        return args
