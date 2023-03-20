# -*- coding: utf-8 -*-
# @Time     : 2023/02/23 16:00:38
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : strategy_three.py
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

计算倍投策略在指定赛季指定球队组合的策略收益情况。通过过滤投入的最大值，用以筛选满足条件的进球数。

评价方式：
1. 如果单次投入最大值超过指定阈值，则过滤掉该进球数
2. 排序筛选获利最大的进球数
"""

import sys
import math
import multiprocessing
from tqdm import tqdm
from NextBFootBallAnalysis.libs.constant import (
    CLUB_NAME_MAPPING,
    STATICS_TYPE_FULL,
    LEAGUES_MAPPING,
)
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from .strategy_common import read_config


def simulation(datas, param, config):
    statics_type = param.get("statics_type")
    goals = int(param.get("goals", ["0"])[0])
    statics_datas = list()
    initial_amount = config.get("INITIAL_AMOUNT")
    multiple = config.get("MULTIPLE")
    threshold = config.get("THRESHOLD")
    max_costs = config.get("MAX_COSTS", 10240)
    odds = config.get("ODDS", {}).get(str(goals), 3.0)
    # 初始资金
    amount = initial_amount
    for data in datas:
        # 如果单次投注已经超过阈值，则不再对后续数据进行计算
        if amount > max_costs:
            return None
        # [投注金额,单次盈利金额]
        statics_data = list()
        if STATICS_TYPE_FULL == statics_type:
            tg = data.ftg
        else:
            tg = data.htg
        if tg < 0:
            continue
        # 超过7球的，统一记为7球
        if tg > 7:
            tg = 7
        # 输
        if goals != tg:
            statics_data.append(amount)
            statics_data.append(-amount)
            amount = amount * multiple
        # 赢
        else:
            # 如果投注金额小于等于THRESHOLD，继续倍投
            if amount <= threshold:
                statics_data.append(amount)
                statics_data.append(amount * odds - amount)
                amount = amount * multiple
            else:
                statics_data.append(amount)
                statics_data.append(amount * odds - amount)
                amount = initial_amount
        statics_datas.append(statics_data)
    # 统计投入
    costs = [p[0] for p in statics_datas]
    # 统计盈利
    profits = [p[1] for p in statics_datas]
    # 正确场次
    correct_count = len([p for p in profits if p > 0])

    # 连续最大投入成本
    max_cost = max(costs)
    n = int(math.log(int(max_cost / initial_amount), 2)) + 1
    sum_max_cost = 0
    for i in range(0, n):
        sum_max_cost += 10 * 2**i
    # 总收益
    total_profit = int(sum(profits))
    # 收益率
    profit_ratio = total_profit / sum_max_cost * 100

    return [
        str(correct_count),
        str(n),
        str(sum_max_cost),
        str(total_profit),
        "%.2f" % profit_ratio,
    ]

def mutil_simulation(epl_teams, others_teams, param, config):
    season = param.get("season", ["2022-2023"])[0]
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    datas = list()
    for e0_team in tqdm(
        epl_teams,
        unit="team",
        desc="英超",
        position=0,
        leave=False,
    ):
        # for i1_team in others_teams["I1"]:
        for i1_team in tqdm(
            others_teams["I1"],
            unit="team",
            desc="意甲",
            position=1,
            leave=False,
        ):
            for sp1_team in others_teams["SP1"]:
            # for sp1_team in tqdm(
            #     others_teams["SP1"],
            #     unit="team",
            #     desc="西甲",
            #     position=2,
            #     leave=False,
            # ):
                for f1_team in others_teams["F1"]:
                # for f1_team in tqdm(
                #     others_teams["F1"],
                #     unit="team",
                #     desc="法甲",
                #     position=3,
                #     leave=False,
                # ):
                    for d1_team in others_teams["D1"]:
                    # for d1_team in tqdm(
                    #     others_teams["D1"],
                    #     unit="team",
                    #     desc="德甲",
                    #     position=4,
                    #     leave=False,
                    # ):
                        merge_teamd = [e0_team, i1_team, sp1_team, d1_team, f1_team]
                        team_sql_data = nfs.get_team_season_matchs(
                            teams=merge_teamd, season=[season]
                        )
                        recommend_data = simulation(team_sql_data, param, config)
                        if recommend_data is None:
                            continue
                        team_names = [
                            CLUB_NAME_MAPPING_TRANSFER.get(ct, ct) for ct in merge_teamd
                        ]
                        recommend_data.insert(0, "|".join(team_names))
                        datas.append(",".join(recommend_data))
    return datas

def strategy_three(param):
    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    try:
        from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
    except:
        sys.exit(0)
    season = param.get("season", ["2022-2023"])[0]
    statics_type = param.get("statics_type")
    goals = param.get("goals", ["0"])[0]
    config_name = param.get("config")
    config = read_config(config_name)
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    current_teams = dict()
    # 获取当前赛季各大联赛参赛球队列表
    for _, div in LEAGUES_MAPPING.items():
        # 查询本赛季参赛球队列表
        current_teams[div] = nfs.get_season_teams(div, season)
    nfs.close_session()
    nfs.close()
    max_workers = 10
    e0_teams = current_teams["E0"]
    # 单进程
    # datas = mutil_simulation(e0_teams, current_teams, param, config)
    # 多进程
    datas = list()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        all_task = [
            executor.submit(
                mutil_simulation, e0_teams[k : k + 2], current_teams, param, config
            )
            for k in range(0, len(e0_teams), 2)
        ]
        wait(all_task, return_when=ALL_COMPLETED)
        for task in all_task:
            result = task.result()
            datas.extend(result)
    statics_type_str = "半场进球"
    if statics_type == STATICS_TYPE_FULL:
        statics_type_str = "全场进球"
    file_name = "nextb_{}_{}_{}进球筛选结果.csv".format(statics_type_str, season, goals)
    headers = "球队组合,正确场次,最大间隔场次,最大投入,总收益,收益率\n"
    data_str = "\n".join(datas)
    with open(file_name, "w", encoding="utf8") as f:
        f.write(headers)
        f.write(data_str)
