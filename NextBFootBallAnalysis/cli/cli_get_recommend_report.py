# -*- coding: utf-8 -*-
# @Time     : 2023/01/12 16:16:17
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_recommend_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_recommend_report


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-recommend-report",
        description="NextB获取推荐球队报告。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-recommend-report -n $number",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="指定获取最近N轮比赛的统计结果,默认最近10轮比赛.",
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
    print(get_recommend_report(param))
