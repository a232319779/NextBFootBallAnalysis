# -*- coding: utf-8 -*-
# @Time     : 2023/01/17 11:04:51
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_team.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from prettytable import PrettyTable
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_team


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-team-match",
        description="NextB获取指定球队最近N场比赛结果。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-team-match -t $team_name",
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
    }
    datas = get_team(param)
    x = PrettyTable()
    x.field_names = ["比赛时间", "主队", "客队", "半场比分", "全场比分"]
    x.add_rows(datas)
    print(x)
