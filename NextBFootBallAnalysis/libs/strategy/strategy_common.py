# -*- coding: utf-8 -*-
# @Time     : 2023/02/23 11:12:59
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : strategy_common.py
# @Software : Visual Studio Code
# @WeChat   : NextB

__doc__ = """
读取策略配置参数。
"""

import json


def read_config(file_name):
    if file_name == "":
        return {
            # 2023.02.15中国体彩全场进球赔率
            "ODDS": {
                "0": 9.5,
                "1": 4.25,
                "2": 3.25,
                "3": 3.9,
                "4": 6.5,
                "5": 11.5,
                "6": 30.0,
                "7": 40.0,
            },
            "INITIAL_AMOUNT": 10,
            "MULTIPLE": 2.0,
            "THRESHOLD": 40,
            "MAX_COSTS": 10240,
        }
    with open(file_name, "r", encoding="utf8") as f:
        data = f.read()
    return json.loads(data)
