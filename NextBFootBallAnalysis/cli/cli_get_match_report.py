# -*- coding: utf-8 -*-
# @Time     : 2023/01/04 16:58:45
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_match_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_match_report


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-match-report",
        description="NextB获取指定两支球队的比赛分析报告。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-match-report -h $home_team -a $away_team",
    )
    parser.add_argument(
        "-ht",
        "--home-team",
        help="指定主队名称.",
        type=str,
        dest="home_team",
        action="store",
        default="",
    )
    parser.add_argument(
        "-at",
        "--away-team",
        help="指定主队名称.",
        type=str,
        dest="away_team",
        action="store",
        default="",
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
    if args.home_team == "" or args.away_team == "":
        print("交战双方不能为空。")
        exit(0)
    param = {
        "home_team": args.home_team,
        "away_team": args.away_team,
        "number": args.number,
        "statics_type": args.statics_type,
    }
    print(get_match_report(param))
