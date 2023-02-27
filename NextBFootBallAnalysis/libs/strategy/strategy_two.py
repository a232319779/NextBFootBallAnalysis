# -*- coding: utf-8 -*-
# @Time     : 2023/02/22 17:54:37
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : strategy_one.py
# @Software : Visual Studio Code
# @WeChat   : NextB

__doc__ = """
投注条件：
        假设赔率固定，取中国体彩赔率
策略一：买进球数
    1. 起投10元
    2. 输：则倍投
    3. 赢：
        a. 小于等于40元则倍投
        b. 大于40元则重新投注

计算倍投策略在指定赛季指定球队的策略收益情况。通过过滤投入的最大值，用以筛选满足条件的进球数。

评价方式：
1. 如果单次投入最大值超过指定阈值，则过滤掉该进球数
2. 排序筛选获利最大的进球数
"""

from NextBFootBallAnalysis.libs.constant import (
    CLUB_NAME_MAPPING,
    STATICS_TYPE_FULL,
    LEAGUES_MAPPING,
)
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from .strategy_common import read_config


def check_teams(input_teams, season_teams, season):
    """
    检查球队是否在该赛季
    """
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    a_set = set(input_teams)
    b_set = set(season_teams)
    c_set = a_set & b_set
    if len(c_set) == len(input_teams):
        return True
    else:
        print(
            "{}未参与{}赛季。".format(
                ",".join(
                    [CLUB_NAME_MAPPING_TRANSFER.get(t, t) for t in list(a_set - c_set)]
                ),
                season,
            )
        )


def simulation_season(datas, goals, statics_type, config):
    statics_datas = list()
    initial_amount = config.get("INITIAL_AMOUNT")
    multiple = config.get("MULTIPLE")
    threshold = config.get("THRESHOLD")
    odds = config.get("ODDS", {}).get(str(goals), 3.0)
    # 初始资金10元
    amount = initial_amount
    total_amount = 0.0
    total_profit = 0.0
    for data in datas:
        # [投注时间,投注金额,单次盈利金额,累计投注,总盈利金额]
        statics_data = list()
        if STATICS_TYPE_FULL == statics_type:
            tg = data.ftg
        else:
            tg = data.htg
        if tg < 0:
            continue
        statics_data.append(data.date_time.strftime("%Y-%m-%d"))
        # 超过7球的，统一记为7球
        if tg > 7:
            tg = 7
        # 输
        if goals != tg:
            statics_data.append(amount)
            statics_data.append(-amount)
            total_amount += amount
            statics_data.append(total_amount)
            total_profit += -amount
            statics_data.append(total_profit)
            amount = amount * multiple
        # 赢
        else:
            # 计算本次盈利
            total_profit += amount * odds - amount
            # 如果投注金额小于等于THRESHOLD，继续倍投
            if amount <= threshold:
                statics_data.append(amount)
                statics_data.append(amount * odds - amount)
                amount = amount * multiple
                total_amount += amount
                statics_data.append(total_amount)
            else:
                statics_data.append(amount)
                statics_data.append(amount * odds - amount)
                total_amount += amount
                statics_data.append(total_amount)
                amount = initial_amount
                total_amount = 0
            # 添加到末尾
            statics_data.append(total_profit)
        statics_datas.append(statics_data)

    return statics_datas


def write_csv(teams_str, statics_type_str, season_str, goals, max_costs, out_datas):
    headers = "比赛时间,进球数,投注金额,总投注金额,盈利金额\n"
    goals_str = "+".join(goals)
    file_name = "{}_{}_{}_{}.csv".format(
        teams_str, statics_type_str, season_str, goals_str
    )
    with open(file_name, "w", encoding="utf8") as f:
        f.write(headers)
        for goal in goals:
            goal = int(goal)
            # 只记录[0,7]区间内的值
            if goal > 7 or goal < 0:
                continue
            for od in out_datas[goal]:
                # 总投入超过1万的，直接过滤掉
                if od[3] > max_costs:
                    continue
                tmp = [od[0], str(goal), str(od[1]), str(od[3]), str(od[4])]
                f.write(",".join(tmp))
                f.write("\n")


def write__flourish(
    teams_str, statics_type_str, season_str, goals, max_costs, out_datas
):
    goals_str = "+".join(goals)
    file_name = "{}_{}_{}_{}_flourish.csv".format(
        teams_str, statics_type_str, season_str, goals_str
    )
    flourish_headers = "标签,{}\n".format(
        ",".join([str(p[0]) for p in out_datas[int(goals[0])]])
    )
    with open(file_name, "w", encoding="utf8") as f:
        f.write(flourish_headers)
        for goal in goals:
            goal = int(goal)
            # 只记录[0,7]区间内的值
            if goal > 7 or goal < 0:
                continue
            costs_int_data = [p[1] for p in out_datas[goal]]
            # 单次投入超过1万的，直接过滤掉
            if max(costs_int_data) > max_costs:
                continue
            costs_data = [str(p) for p in costs_int_data]
            profits_total_data = [str(p[4]) for p in out_datas[goal]]
            costs_data_str = "{}球投入金额,{}\n".format(goal, ",".join(costs_data))
            profits_total_data_str = "{}球总盈利金额,{}\n".format(
                goal, ",".join(profits_total_data)
            )
            f.write(costs_data_str)
            f.write(profits_total_data_str)


def strategy_two(param):
    teams = param.get("teams")
    season = param.get("season", ["2022-2023"])
    statics_type = param.get("statics_type")
    goals = param.get("goals")
    config_name = param.get("config")
    config = read_config(config_name)
    max_costs = config.get("MAX_COSTS", 10240)
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    statics_type_str = "半场进球"
    if statics_type == STATICS_TYPE_FULL:
        statics_type_str = "全场进球"
    # 输出球队
    english_team = [CLUB_NAME_MAPPING.get(t, t) for t in teams]
    # 获取当前赛季各大联赛参赛球队列表
    current_teams = list()
    for _, div in LEAGUES_MAPPING.items():
        # 查询本赛季参赛球队列表
        current_teams.extend(nfs.get_season_teams(div, season[0]))
    check_teams(english_team, current_teams, season[0])
    datas = nfs.get_team_season_matchs(teams=english_team, season=season)
    out_datas = dict()
    for goal in goals:
        goal = int(goal)
        # 过滤非正常比分
        if goal < 0:
            continue
        if goal not in out_datas.keys():
            out_datas[goal] = list()
        s_data = simulation_season(
            datas=datas, goals=goal, statics_type=statics_type, config=config
        )
        out_datas[goal].extend(s_data)

    teams_str = "+".join(teams)
    season_str = "+".join(season)
    # 输出为flourish格式的csv
    write__flourish(
        teams_str, statics_type_str, season_str, goals, max_costs, out_datas
    )
    # 输出为普通csv格式
    write_csv(teams_str, statics_type_str, season_str, goals, max_costs, out_datas)
    nfs.close_session()
    nfs.close()
