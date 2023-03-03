# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:10:29
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : common.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import os
import datetime
from tqdm import tqdm
from collections import Counter
from statistics import mean, median, variance
from dateutil.relativedelta import relativedelta
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from NextBFootBallAnalysis.libs.constant import (
    YEARS_MAPPING,
    CLUB_NAME_MAPPING,
    DEFAULT_MATCHS_NUMBER,
    LEAGUES_MAPPING,
)


def get_file_list(file_dir):
    """
    遍历指定目录，获取文件路径
    """
    file_paths = list()
    for root, _, files in os.walk(file_dir):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))

    return file_paths


def read_datas(file_name):
    """
    从文件读取数据
    """
    with open(file_name, "r", encoding="windows-1252") as f:
        datas = f.readlines()

    # 过滤空行
    return [data for data in datas if not data.startswith(",,,,")]


def format_date(data, has_time=False):
    """
    标准化赛季时间，例如从 01/01/93 -> 01/01/1993
    """
    # 默认只获取date值
    key_index = [1]
    date_format = "%d/%m/%Y"
    # 后面的赛季加入了比赛时间,Time
    if has_time:
        key_index = [1, 2]
        date_format = "%d/%m/%Y %H:%M"
    tmp = data.split(",")
    # 用于可能的时间拼接，如： date + time
    date = list()
    for ki in key_index:
        for y in YEARS_MAPPING.keys():
            # 判断第6-8位是否是需要映射的年份
            if tmp[ki][6:8] == y and len(tmp[ki].split("/")[-1]) == 2:
                tmp[ki] = tmp[ki][:6] + YEARS_MAPPING[y]
                break
        # 第一次是date，第二次是time
        date.append(tmp[ki])
    date_str = " ".join(date)
    date_obj = datetime.datetime.strptime(date_str, date_format)
    return date_obj


def format_list(data, ratio_key):
    """
    ratio_key: value的名称
    目前仅用于格式化进球场次统计
    """
    ratio_data = data.get(ratio_key)
    format_list = list()
    # total_len = [len(t) for t in ratio_data.values()]
    # total = sum(total_len)
    for key, value in ratio_data.items():
        if key not in [0, 1, 2, 3]:
            continue
        value_new = sorted(value)
        # 统计进球场次最大间隔
        max_dist = max(value_new)
        # 统计进球场次最小间隔
        min_dist = min(value_new)
        # 统计进球场次平均间隔
        mean_dist = "%.2f" % mean(value_new)
        # 统计进球场次中位数间隔
        median_dist = median(value_new)
        # 统计每个进球场次间隔的占比
        counter_str_list = list()
        counter = Counter(value)
        total = sum(counter.values())
        index = 0
        for a, b in counter.most_common():
            b1 = "%.2f" % (b / total)
            counter_str_list.append("{}-{}".format(str(a), str(b1)))
            index += 1
            # 只看top5的
            if index >= 5:
                break
        format_list.append("\n\t进{}球最大间隔:{}场".format(str(key), max_dist))
        format_list.append("\n\t进{}球最小间隔:{}场".format(str(key), min_dist))
        format_list.append("\n\t进{}球平均间隔:{}场".format(str(key), mean_dist))
        format_list.append("\n\t进{}球中位数间隔:{}场".format(str(key), median_dist))
        format_list.append(
            "\n\t进{}球出现场次及占比:{}".format(str(key), ",".join(counter_str_list))
        )
    # format_list.sort()
    return ", ".join(format_list)


def parse_raw(data, has_time=False):
    """
    输入数据解析格式
    Div: tmp[0], 联赛名称
    Date: tmp[1], 比赛日期
    Time: tmp[2], 比赛时间
    HomeTeam: tmp[2]/tmp[3], 主队名称
    AwayTeam: tmp[3]/tmp[4], 客队名称
    FTHG: tmp[4]/tmp[5], 全场主队进球
    FTAG: tmp[5]/tmp[6], 全场客队进球
    FTR: tmp[6]/tmp[7], 全场比赛结果, H: 主队胜, A: 客队胜, D: 平局
    HTHG: tmp[7]/tmp[8], 半场场主队进球
    HTAG: tmp[8]/tmp[9], 半场场客队进球
    HTR: tmp[9]/tmp[10], 半场比赛结果, H: 主队胜, A: 客队胜, D: 平局
    输出结果为列表，每个元素为字典，包含以下字段：
    div: 联赛名称
    season: 赛季
    date_time: 比赛时间
    home_team: 主队名称
    away_team: 客队名称
    fthg: 全场主队进球
    ftag: 全场客队进球
    ftg: 全场进球数
    ftr: 全场比赛结果, H: 主队胜, A: 客队胜, D: 平局
    hthg: 半场场主队进球
    htag: 半场场客队队进球
    htg: 半场进球数
    htr: 半场场比赛结果, H: 主队胜, A: 客队胜, D: 平局
    """
    data_keys = [
        "div",
        "date_time",
        "home_team",
        "away_team",
        "fthg",
        "ftag",
        "ftg",
        "ftr",
        "hthg",
        "htag",
        "htg",
        "htr",
    ]
    # 缺省值填充-1
    data_values = [-1] * len(data_keys)
    # 对应值偏移, 不包含time时, 偏移为0, 否则偏移需要加1
    offset = 0
    if has_time:
        offset = 1
    # 按逗号分割字符串
    tmp = data.split(",")
    # 联赛名称索引固定为0
    data_values[0] = tmp[0]
    # 比赛时间
    data_values[1] = format_date(data, has_time)
    # 主队名称
    data_values[2] = tmp[2 + offset]
    # 客队名称
    data_values[3] = tmp[3 + offset]
    # 全场主队进球
    data_values[4] = int(tmp[4 + offset])
    # 全场客队进球
    data_values[5] = int(tmp[5 + offset])
    # 全场进球数
    data_values[6] = data_values[4] + data_values[5]
    # 全场比赛结果
    data_values[7] = tmp[6 + offset]
    # 如果有半场比分, 则覆盖
    if len(tmp) > 7 and tmp[7 + offset] != "":
        # 半场主队进球
        data_values[8] = int(tmp[7 + offset])
        # 半场客队进球
        data_values[9] = int(tmp[8 + offset])
        # 半场进球数
        data_values[10] = data_values[8] + data_values[9]
        # 半场比赛结果
        data_values[11] = tmp[9 + offset]
    # 没有半场比分, 则将半场比赛结果填充为空
    else:
        data_values[11] = ""
    data_dict = dict(zip(data_keys, data_values))
    return data_dict


def parse_data(file_name, number=None):
    """
    解析指定文件格式
    """
    datas = read_datas(file_name)
    has_time = False
    # 后面的赛季加入了比赛时间,Time
    if datas[0].startswith("Div,Date,Time,"):
        has_time = True
    # 删除header
    del datas[0]
    # 生成season
    season_start = format_date(datas[0])
    season_finish = season_start + relativedelta(years=1)
    season = "{}-{}".format(season_start.year, season_finish.year)
    # 解析比赛数据
    out_datas = list()
    if number:
        datas = datas[-number:]
    for data in datas:
        data_dict = parse_raw(data, has_time)
        # 增加赛季
        data_dict["season"] = season
        out_datas.append(data_dict)

    return out_datas


def get_last_matchs(param):
    league = param.get("league")
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    if league:
        if LEAGUES_MAPPING.get(league, None) is None:
            print("输入错误，请输入正确的联赛名称，取值包括：[英超,意甲,西甲,德甲,法甲]")
            exit()
        leagues_mapping = {league: LEAGUES_MAPPING.get(league)}
    else:
        leagues_mapping = LEAGUES_MAPPING
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    for name, div in leagues_mapping.items():
        # 查询联赛最后一场
        matchs = nfs.get_league_last_matchs(div=div, number=1)
        # 未查询到数据
        if not matchs:
            continue
        m = matchs[0]
        # 联赛名称, 赛季, 比赛时间, 主队, 客队, 半场比分, 全场比分
        tmp = list()
        tmp.append(name)
        tmp.append(m.season)
        tmp.append(m.date_time.strftime("%Y/%m/%d %H:%M"))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.home_team, m.home_team))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.away_team, m.away_team))
        tmp.append("{}-{}".format(m.hthg, m.htag))
        tmp.append("{}-{}".format(m.fthg, m.ftag))
        datas.append(tmp)
    nfs.close_session()
    nfs.close()
    return datas


def get_recommend(param):
    """
    推荐原理：
    计算每支球队，每个赛季的进球占比，计算占比方差，选择占比最大，方差最小的前3支球队
    headers: 联赛名称,球队名称,联赛N球占比,比赛场次,球队N球占比,赛季占比,占比方差
    """

    def calc_variance(ct, seasons):
        ratio_list = list()
        for s in seasons:
            # 获取分布统计
            team_group_data = nfs.get_team_goals_group_by(ct, [s])
            count_sum = sum([p[1] for p in team_group_data])
            ratio = 0.0
            for tgd in team_group_data:
                if goals == tgd[0]:
                    count = tgd[1]
                    ratio = round(count / count_sum, 3)
                    break
            ratio_list.append(ratio)
        return variance(ratio_list)

    goals = param.get("goals", 2)
    season = param.get("season", "2022-2023")
    # 球队转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    # 构造全赛季列表
    all_seasons = nfs.create_season_list(season, 30)
    datas = dict()
    for name, div in tqdm(LEAGUES_MAPPING.items(), unit="联赛", desc="联赛计算中"):
        if div not in datas.keys():
            datas[div] = list()
        # 获取指定联赛指定赛季参赛球队
        current_teams = nfs.get_season_teams(div, season)
        if len(current_teams) == 0:
            continue
        # 计算联赛N进球占比
        div_goals = nfs.get_div_goals_group_by(div, all_seasons)
        div_goals_sum = sum([p[1] for p in div_goals])
        div_goals_ratio = 0.0
        for dg in div_goals:
            if goals == dg[0]:
                count = dg[1]
                div_goals_ratio = round(count / div_goals_sum, 3)
        # 按联赛球队统计数据
        for ct in tqdm(current_teams, unit="球队", desc="球队计算中"):
            # 球队总进球占比
            team_goals = nfs.get_team_goals_group_by(ct, all_seasons)
            team_goals_sum = sum([p[1] for p in team_goals])
            team_goals_ratio = 0.0
            for dg in team_goals:
                if goals == dg[0]:
                    count = dg[1]
                    team_goals_ratio = round(count / team_goals_sum, 3)
            # 球队占比低于历史占比，则不要
            if team_goals_ratio - div_goals_ratio <= 0:
                continue
            # 计算主场进球占比
            home_goals = nfs.get_home_team_goals_group_by(ct, all_seasons[-3:])
            home_goals_sum = sum([p[1] for p in home_goals])
            home_goals_ratio = 0.0
            for dg in home_goals:
                if goals == dg[0]:
                    count = dg[1]
                    home_goals_ratio = round(count / home_goals_sum, 3)
            # 计算客场进球占比
            away_goals = nfs.get_away_team_goals_group_by(ct, all_seasons[-3:])
            away_goals_sum = sum([p[1] for p in away_goals])
            away_goals_ratio = 0.0
            for dg in away_goals:
                if goals == dg[0]:
                    count = dg[1]
                    away_goals_ratio = round(count / away_goals_sum, 3)
            # 球队当前赛季进球占比
            team_season_goals = nfs.get_team_goals_group_by(ct, [all_seasons[-1]])
            team_season_goals_sum = sum([p[1] for p in team_season_goals])
            team_season_goals_ratio = 0.0
            for dg in team_season_goals:
                if goals == dg[0]:
                    count = dg[1]
                    team_season_goals_ratio = round(count / team_season_goals_sum, 3)
            # 计算方差
            t_variance = round(calc_variance(ct, all_seasons), 4)
            team_datas = list()
            team_datas.append(name)
            team_datas.append(CLUB_NAME_MAPPING_TRANSFER.get(ct, ct))
            team_datas.append(div_goals_ratio)
            team_datas.append(team_goals_sum)
            team_datas.append(team_goals_ratio)
            team_datas.append(home_goals_ratio)
            team_datas.append(away_goals_ratio)
            team_datas.append(team_season_goals_ratio)
            team_datas.append(t_variance)
            datas[div].append(team_datas)
        datas[div].sort(key=lambda x: x[8])
        # 只要筛选出来的前3个
        datas[div] = datas[div][:3]
    nfs.close_session()
    nfs.close()
    return datas


def get_team(param):
    team_ori = param.get("team")
    team = CLUB_NAME_MAPPING.get(team_ori, team_ori)
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    number = param.get("number", DEFAULT_MATCHS_NUMBER)
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    match_datas = nfs.get_team_last_matchs(team=team, number=number)
    for m in match_datas:
        tmp = list()
        tmp.append(m.date_time.strftime("%Y/%m/%d %H:%M"))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.home_team, m.home_team))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.away_team, m.away_team))
        tmp.append("{}-{}".format(m.hthg, m.htag))
        tmp.append("{}-{}".format(m.fthg, m.ftag))
        datas.append(tmp)
    datas.reverse()
    return datas

def get_match(param):
    teams = param.get("teams")
    home_team_ori = teams[0]
    away_team_ori = teams[1]
    season = param.get("season")
    home_team = CLUB_NAME_MAPPING.get(home_team_ori, home_team_ori)
    away_team = CLUB_NAME_MAPPING.get(away_team_ori, away_team_ori)
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    # 构造全赛季列表
    all_seasons = nfs.create_season_list(season, 30)
    # 历史比赛记录
    match_datas_1 = nfs.get_team_match_goals_group_by(hteam=home_team, ateam=away_team, seasons=all_seasons)
    match_datas_2 = nfs.get_team_match_goals_group_by(hteam=away_team, ateam=home_team, seasons=all_seasons)
    # 统计进球数
    for goal in range(0, 20):
        d1 = 0
        d2 = 0
        total = 0
        data = list()
        for md1 in match_datas_1:
            if md1[0] == goal:
                d1 = md1[1]
                break
        for md2 in match_datas_2:
            if md2[0] == goal:
                d2 = md2[1]
                break
        total = d1 + d2
        if total == 0:
            continue
        m = nfs.get_last_goal_match(home_team, away_team, goal)
        data.append(goal)
        data.append(total)
        data.append(d1)
        data.append(d2)
        if m:
            data.append(m.date_time.strftime("%Y/%m/%d %H:%M"))
        else:
            data.append("未出现过该进球数")
        if m.fthg > m.ftag:
            data.append("{}（主胜）".format(CLUB_NAME_MAPPING_TRANSFER.get(m.home_team)))
        elif m.fthg < m.ftag:
            data.append("{}（客胜）".format(CLUB_NAME_MAPPING_TRANSFER.get(m.away_team)))
        else:
            data.append("平局")
        datas.append(data)
    datas.sort(key=lambda x: x[1], reverse=True)
    return datas
