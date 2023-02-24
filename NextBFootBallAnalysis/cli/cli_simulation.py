# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 16:04:33
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_simulation.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.strategy.strategy_one import strategy_one
from NextBFootBallAnalysis.libs.strategy.strategy_two import strategy_two
from NextBFootBallAnalysis.libs.strategy.strategy_three import strategy_three


__doc__ = """
NextB的足球数据彩票投注仿真程序。
"""


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-simulation",
        description="NextB基于足球数据的彩票投注仿真程序。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-simulation",
    )
    parser.add_argument(
        "-t",
        "--teams",
        nargs="+",
        help="指定球队名称",
        dest="teams",
        action="store",
        default=["阿森纳"],
    )
    parser.add_argument(
        "-f",
        "--func",
        help="指定统计方法，支持[one: 输出收益随策略开始时间的关系, two: 输出指定赛季指定球队的策略收益, three: 输出组合结果]",
        type=str,
        dest="function",
        action="store",
        default="two",
    )

    parser.add_argument(
        "-n",
        "--number",
        help="指定最近的比赛场次数量。默认最近500场比赛。适用于func: one，统计方法。",
        type=int,
        dest="number",
        action="store",
        default=500,
    )

    parser.add_argument(
        "-s",
        "--season",
        help="指定赛季名称。默认为2022-2023赛季，赛季格式如：2022-2023。适用于func: two统计方法。",
        nargs="+",
        dest="season",
        action="store",
        default=["2022-2023"],
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
    parser.add_argument(
        "-g",
        "--goals",
        help="指定仿真计算的进球数量，可选值包括[0,1,2,3,4,5,6,7]，自动忽略其他值默认为：1球",
        nargs="+",
        dest="goals",
        action="store",
        default=["1"],
    )
    parser.add_argument(
        "-c",
        "--config",
        help="指定回测参数，如：赔率、投注方式等",
        type=str,
        dest="config",
        action="store",
        default="",
    )

    args = parser.parse_args()

    return args


func = {"one": strategy_one, "two": strategy_two, "three": strategy_three}


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    params = {
        "teams": args.teams,
        "number": args.number,
        "statics_type": args.statics_type,
        "goals": args.goals,
        "config": args.config,
        "season": args.season,
    }
    func[args.function](params)
