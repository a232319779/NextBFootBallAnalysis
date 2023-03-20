# -*- coding: utf-8 -*-
# @Time     : 2023/03/02 19:21:01
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_match.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from prettytable import PrettyTable
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_match


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-match",
        description="NextB获取指定两支球队的进球分析。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-match -ht $home_team -at away_team",
    )
    parser.add_argument(
        "-t",
        "--teams",
        help="指定球队名称。指定2支球队名称，超过2支则取前2支球队。默认值：['切尔西', '曼联']",
        nargs="+",
        dest="teams",
        action="store",
        default=["切尔西", "曼联"],
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

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "teams": args.teams,
        "season": args.season,
    }
    datas = get_match(param)
    x = PrettyTable()
    x.field_names = [
        "进球数",
        "总场次",
        "主:{}".format(args.teams[0]),
        "主:{}".format(args.teams[1]),
        "最近一场",
        "比赛结果"
    ]
    x.add_rows(datas)
    print(x)
