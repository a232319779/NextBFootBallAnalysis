# -*- coding: utf-8 -*-
# @Time     : 2023/01/16 12:37:16
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_recommend.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from prettytable import PrettyTable
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_recommend


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-recommend",
        description="NextB生成球队推荐结果。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-recommend",
    )
    parser.add_argument(
        "-s",
        "--season",
        help="指定赛季名称。默认为2022-2023赛季，赛季格式如：2022-2023。",
        type=str,
        dest="season",
        action="store",
        default="2022-2023",
    )
    parser.add_argument(
        "-g",
        "--goals",
        help="指定进球数量，可选值包括[0,1,2,3,4,5,6,7]，自动忽略其他值默认为：2球",
        type=int,
        dest="goals",
        action="store",
        default=2,
    )
    parser.add_argument(
        "-st",
        "--statics_type",
        help="指定进球统计类型,可选值包括[0: 半场, 1: 全场],默认值为: 1,统计全场进球数.",
        type=int,
        dest="statics_type",
        action="store",
        default=1,
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "season": args.season,
        "goals": args.goals,
        "statics_type": args.statics_type,
    }
    datas = get_recommend(param)
    x = PrettyTable()
    x.field_names = [
        "联赛名称",
        "半全场",
        "球队名称",
        "联赛{}球占比".format(args.goals),
        "比赛场次",
        "球队{}球占比".format(args.goals),
        "主场{}球占比".format(args.goals),
        "客场{}球占比".format(args.goals),
        "{}".format(args.season),
        "占比方差",
    ]
    for _, data in datas.items():
        x.add_rows(data)
    print(x)
