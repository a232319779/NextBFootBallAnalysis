# -*- coding: utf-8 -*-
# @Time     : 2023/01/11 10:11:56
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_statics_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from prettytable import PrettyTable
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
        help="获取指定联赛的最后一场比赛信息,默认获取5大联赛的最后一场比赛信息.取值包括：[英超,意甲,西甲,德甲,法甲]",
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
    datas = get_statics_report(param)
    x = PrettyTable()
    x.field_names = ["联赛名称", "赛季", "比赛时间", "主队", "客队", "半场比分", "全场比分"]
    x.add_rows(datas)
    print(x)
