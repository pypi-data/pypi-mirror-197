#!/usr/bin/python3
# coding:utf-8
# Copyright (c) 2023 ZouMingzhe <zoumingzhe@qq.com>

from xarg import xarg


def main():
    _arg = xarg("xarg-hello")
    _arg.add_opt("-x")
    _arg.add_opt("-arg")
    _arg.add_opt("-o", "--opt")
    _arg.add_opt_on("--opt-on")
    _arg.add_opt_off("--opt-off")
    _arg.add_pos("pos_1", 1)
    _arg.add_pos("pos_2", 2)
    _arg.add_pos("pos_0_or_1", 0)
    _arg.add_pos("pos_n", -1)
    print(_arg.parse_args())
