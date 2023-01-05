# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 18:55:34
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_team_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_report


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-team-report",
        description="NextB获取指定球队的分析报告。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-team-report -n $team_name",
    )
    parser.add_argument(
        "-t",
        "--team",
        help="指定球队名称,默认值为: 阿森纳.",
        type=str,
        dest="team",
        action="store",
        default="阿森纳",
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
        "-x",
        "--xnumber",
        help="指定最近X个赛季的数目,默认最近5个赛季.",
        type=int,
        dest="xnumber",
        action="store",
        default=5,
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
        "team": args.team,
        "number": args.number,
        "xnumber": args.xnumber,
        "statics_type": args.statics_type,
    }
    print(get_report(param))
