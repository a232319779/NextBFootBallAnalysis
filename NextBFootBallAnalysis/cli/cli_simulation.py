# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 16:04:33
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_init_football_db.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import math
import argparse
from tqdm import tqdm
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.constant import CLUB_NAME_MAPPING, STATICS_TYPE_FULL
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB

__doc__ = """
投注条件：
    假设赔率固定为：2.3

投注策略：
1. 起投10元
2. 输：则倍投
3. 赢：
    a. 小于等于40元则倍投
    b. 大于40元则重新投注
"""

ODDS = 2.3
INITIAL_AMOUNT = 10
MULTIPLE = 2.0
THRESHOLD = 40


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
        # type=list,
        dest="teams",
        action="store",
        default=None,
    )

    parser.add_argument(
        "-n",
        "--number",
        help="指定最近的比赛场次数量。默认最近500场比赛。",
        type=int,
        dest="number",
        action="store",
        default=500,
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
    parser.add_argument(
        "-g",
        "--goals",
        help="指定仿真计算的进球数量，默认为：1球",
        type=int,
        dest="goals",
        action="store",
        default=1,
    )

    args = parser.parse_args()

    return args


def simulation(datas, goals, statics_type):
    statics_datas = list()
    # 初始资金10元
    amount = INITIAL_AMOUNT
    start_time = ""
    for data in datas:
        # [投注金额,盈利金额]
        statics_data = list()
        if STATICS_TYPE_FULL == statics_type:
            tg = data.ftg
        else:
            tg = data.htg
        if tg < 0:
            continue
        if start_time == "":
            start_time = data.date_time.strftime("%Y-%m-%d")
        # 输
        if goals != tg:
            statics_data.append(amount)
            statics_data.append(-amount)
            amount = amount * MULTIPLE
        # 赢
        else:
            # 如果投注金额小于等于THRESHOLD，继续倍投
            if amount <= THRESHOLD:
                statics_data.append(amount)
                statics_data.append(amount * ODDS - amount)
                amount = amount * MULTIPLE
            else:
                statics_data.append(amount)
                statics_data.append(amount * ODDS - amount)
                amount = INITIAL_AMOUNT
        statics_datas.append(statics_data)

    # 统计投入
    costs = [p[0] for p in statics_datas]
    # 统计盈利
    profits = [p[1] for p in statics_datas]
    # 正确场次
    correct_count = len([p for p in profits if p > 0])

    # 连续最大投入成本
    max_cost = max(costs)
    n = int(math.log(int(max_cost / INITIAL_AMOUNT), 2)) + 1
    sum_max_cost = 0
    for i in range(0, n):
        sum_max_cost += 10 * 2**i
    # 总收益
    total_profit = int(sum(profits))
    # 收益率
    profit_ratio = total_profit / sum_max_cost * 100

    return [
        start_time,
        str(correct_count),
        str(n),
        str(sum_max_cost),
        str(total_profit),
        "%.2f" % profit_ratio,
    ]


def start(param):
    teams = param.get("teams", [])
    number = param.get("number")
    statics_type = param.get("statics_type")
    goals = param.get("goals")
    csv_datas = list()
    date_times = list()
    costs_data = list()
    profits_data = list()
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    english_teams = [CLUB_NAME_MAPPING.get(t, t) for t in teams]
    match_datas = nfs.get_mergeteams_matchs(english_teams, number=number)
    data_len = len(match_datas)
    statics_type_str = "半场进球"
    if statics_type == STATICS_TYPE_FULL:
        statics_type_str = "全场进球"
    for i in tqdm(range(0, data_len), unit="team", desc="NexBFootBall投注仿真计算中"):
        datas = match_datas[-data_len + i :]
        s_data = simulation(datas=datas, goals=goals, statics_type=statics_type)
        csv_data = [s_data[0], statics_type_str, str(goals), str(data_len - i)]
        csv_data.extend(s_data[1:])
        csv_datas.append(",".join(csv_data))
        date_times.append(csv_data[0])
        costs_data.append(csv_data[6])
        profits_data.append(csv_data[7])
    nfs.close_session()
    nfs.close()

    headers = "起始时间,投注类型,投注进球数,投注场数,正确场次,连续错误最大场次,投注金额,盈利金额,收益率\n"
    team_names = "+".join(teams)
    file_name = "{}_{}.csv".format(team_names, goals)
    with open(file_name, "w", encoding="utf8") as f:
        f.write(headers)
        f.write("\n".join(csv_datas))
    team_names = "+".join(teams)
    file_name = "{}_{}_flourish.csv".format(team_names, goals)
    flourish_headers = "标签,{}\n".format(",".join(date_times))
    costs_data_str = "最大投入金额,{}\n".format(",".join(costs_data))
    profits_data_str = "盈利金额,{}\n".format(",".join(profits_data))
    with open(file_name, "w", encoding="utf8") as f:
        f.write(flourish_headers)
        f.write(costs_data_str)
        f.write(profits_data_str)


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
    }
    start(params)
