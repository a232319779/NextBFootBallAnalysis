# -*- coding: utf-8 -*-
# @Time     : 2023/01/11 10:11:56
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_statics_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_statics_report


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-statics-report",
        description="NextB获取统计分析报告。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-statics-report -n $number",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="指定最近N场比赛的数目,默认最近10场比赛.",
        type=int,
        dest="number",
        action="store",
        default=10,
    )
    parser.add_argument(
        "-st",
        "--statics_type",
        help="指定进球统计类型,可选值包括[0: 半场, 1: 全场],默认值为: 0,统计半场进球数.",
        type=int,
        dest="statics_type",
        action="store",
        default=0,
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "number": args.number,
        "statics_type": args.statics_type,
    }
    print(get_statics_report(param))
