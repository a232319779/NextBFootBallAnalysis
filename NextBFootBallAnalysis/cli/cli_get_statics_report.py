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
        "-l",
        "--league",
        help="获取指定联赛的最后一场比赛信息,默认获取5大联赛的最后一场比赛信息.[E0:英超,I1:意甲,SP1:西甲,D1:德甲,F1:法甲]",
        type=str,
        dest="league",
        action="store",
        default="",
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {"league": args.league}
    print(get_statics_report(param))
