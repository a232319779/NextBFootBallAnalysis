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

from tqdm import tqdm
from NextBFootBallAnalysis.libs.constant import CLUB_NAME_MAPPING, STATICS_TYPE_FULL
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from .strategy_common import read_config


def simulation_season(datas, goals, statics_type, config):
    statics_datas = list()
    initial_amount = config.get("INITIAL_AMOUNT")
    multiple = config.get("MULTIPLE")
    threshold = config.get("THRESHOLD")
    odds = config.get("ODDS", {}).get(str(goals), 3.0)
    # 初始资金10元
    amount = initial_amount
    total_profit = 0.0
    for data in datas:
        # [投注时间,投注金额,单次盈利金额,总盈利金额]
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
            else:
                statics_data.append(amount)
                statics_data.append(amount * odds - amount)
                amount = initial_amount
            # 添加到末尾
            statics_data.append(total_profit)
        statics_datas.append(statics_data)

    return statics_datas


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
    for t in tqdm(teams, unit="team", desc="NextBFootBall投注仿真计算中"):
        english_team = CLUB_NAME_MAPPING.get(t, t)
        datas = nfs.get_team_season_matchs(team=english_team, season=season)
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

        goals_str = "+".join(goals)
        season_str = "+".join(season)
        file_name = "{}_{}_{}_{}_flourish.csv".format(
            t, statics_type_str, season_str, goals_str
        )
        flourish_headers = "标签,{}\n".format(
            ",".join([str(p[0]) for p in out_datas[goal]])
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
                # profits_data = [str(p[2]) for p in out_datas[goal]]
                profits_total_data = [str(p[3]) for p in out_datas[goal]]
                costs_data_str = "{}球投入金额,{}\n".format(goal, ",".join(costs_data))
                # profits_data_str = "{}球单次盈利金额,{}\n".format(goal, ",".join(profits_data))
                profits_total_data_str = "{}球总盈利金额,{}\n".format(
                    goal, ",".join(profits_total_data)
                )
                f.write(costs_data_str)
                # f.write(profits_data_str)
                f.write(profits_total_data_str)
    nfs.close_session()
    nfs.close()
