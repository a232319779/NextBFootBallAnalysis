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
        "-n",
        "--number",
        help="指定总场次数量。默认300场。",
        type=int,
        dest="number",
        action="store",
        default=300,
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

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {"season": args.season, "goals": args.goals, "number": args.number}
    datas, last_n_seasons = get_recommend(param)
    x = PrettyTable()
    x.field_names = [
        "联赛名称",
        "球队名称",
        "总场次",
        "进{}球场次".format(args.goals),
        "总占比",
        "{}赛季".format(last_n_seasons[0]),
        "{}赛季".format(last_n_seasons[1]),
        "{}赛季".format(last_n_seasons[2]),
    ]
    x.add_rows(datas)
    print(x)
