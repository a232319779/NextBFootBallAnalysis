# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:10:29
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : common.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import os
import datetime
from dateutil.relativedelta import relativedelta
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from NextBFootBallAnalysis.libs.constant import (
    YEARS_MAPPING,
    CLUB_NAME_MAPPING,
    TEAM_REPORT,
    MATCH_REPORT,
    MAX_MATCHS_NUMBER,
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
            if tmp[ki][6:8] == y:
                tmp[ki] = tmp[ki][:6] + YEARS_MAPPING[y]
                break
        # 第一次是date，第二次是time
        date.append(tmp[ki])
    date_str = " ".join(date)
    date_obj = datetime.datetime.strptime(date_str, date_format)
    return date_obj


def format_ratio(data, ratio_key):
    """
    ratio_key: value的名称
    """
    ratio_data = data.get(ratio_key)
    total = sum(ratio_data.values())
    format_list = list()
    for key, value in ratio_data.items():
        ratio = "%.2f" % (value / total)
        format_list.append("{}:{}".format(str(key), str(ratio)))
    format_list.sort()
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


def save_csv(datas):
    headers = "Season,Date,HomeTeam,AwayTeam,FTHG,FTAG,HTHG,HTAG,FTG,HTG\n"
    with open("merge.csv", "w", encoding="utf8") as f:
        f.write(headers)
        f.write("\n".join(datas))


def parse_team(matchs, statics_type, **param):
    """
    team: 球队名称
    total_key: 总数key的名称
    ratio_key: 总的分布比例字段名称
    home_ratio_key: 主场分布比例字段名称
    away_ratio_key: 客场分布比例字段名称
    """
    team = param.get("team")
    total = param.get("total_key")
    ratio_key = param.get("ratio_key")
    home_ratio_key = param.get("home_ratio_key")
    away_ratio_key = param.get("away_ratio_key")
    data = {
        total: len(matchs),
        ratio_key: dict(),
        home_ratio_key: dict(),
        away_ratio_key: dict(),
    }
    for match in matchs:
        if 1 == statics_type:
            tg = match.ftg
            score = "{}-{}".format(match.fthg, match.ftag)
        else:
            tg = match.htg
            score = "{}-{}".format(match.hthg, match.htag)
        # 进球数统计
        if tg not in data[ratio_key].keys():
            data[ratio_key][tg] = 0
        data[ratio_key][tg] += 1
        # 比分统计
        if score not in data[ratio_key].keys():
            data[ratio_key][tg] = 0
        data[ratio_key][tg] += 1
        # 主场统计统计
        if team == match.home_team:
            if tg not in data[home_ratio_key].keys():
                data[home_ratio_key][tg] = 0
            data[home_ratio_key][tg] += 1
        # 客场统计统计
        if team == match.away_team:
            if tg not in data[away_ratio_key].keys():
                data[away_ratio_key][tg] = 0
            data[away_ratio_key][tg] += 1

    return data


def get_report(param):
    team_ori = param.get("team")
    team = CLUB_NAME_MAPPING.get(team_ori)
    number = param.get("number")
    xnumber = param.get("xnumber")
    statics_type = param.get("statics_type")
    statics_type_str = "半场进球"
    if 1 == statics_type:
        statics_type_str = "全场进球"

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    # 查询全部比赛
    matchs = nfs.get_team_last_matchs(team=team, number=MAX_MATCHS_NUMBER)
    matchs_data = parse_team(
        matchs,
        team=team,
        statics_type=statics_type,
        total_key="total",
        ratio_key="goals_total_ratio",
        home_ratio_key="home_goals_total_ratio",
        away_ratio_key="away_goals_total_ratio",
    )
    # 查询最近number场比赛
    n_match = nfs.get_team_last_matchs(team=team, number=number)
    n_matchs_data = parse_team(
        n_match,
        team=team,
        statics_type=statics_type,
        total_key="number",
        ratio_key="match_goals_ratio",
        home_ratio_key="home_match_goals_rartio",
        away_ratio_key="away_match_goals_ratio",
    )
    # 查询最近xnumber个赛季比赛
    x_match = nfs.get_team_last_season_matchs(team=team, number=xnumber)
    x_matchs_data = parse_team(
        x_match,
        team=team,
        statics_type=statics_type,
        total_key="xnumber",
        ratio_key="season_goals_ratio",
        home_ratio_key="home_season_goals_ratio",
        away_ratio_key="away_season_goals_ratio",
    )
    nfs.close_session()
    nfs.close()
    home_number = sum(n_matchs_data.get("home_match_goals_rartio").values())
    away_number = sum(n_matchs_data.get("away_match_goals_ratio").values())
    season_total = sum(x_matchs_data.get("season_goals_ratio").values())
    report = TEAM_REPORT.format(
        team=team_ori,
        statics_type_str=statics_type_str,
        total=matchs_data.get("total"),
        goals_total_ratio=format_ratio(matchs_data, "goals_total_ratio"),
        home_goals_total_ratio=format_ratio(matchs_data, "home_goals_total_ratio"),
        away_goals_total_ratio=format_ratio(matchs_data, "away_goals_total_ratio"),
        number=number,
        match_goals_ratio=format_ratio(n_matchs_data, "match_goals_ratio"),
        home_number=home_number,
        home_match_goals_rartio=format_ratio(n_matchs_data, "home_match_goals_rartio"),
        away_number=away_number,
        away_match_goals_ratio=format_ratio(n_matchs_data, "away_match_goals_ratio"),
        xnumber=xnumber,
        season_total=season_total,
        season_goals_ratio=format_ratio(x_matchs_data, "season_goals_ratio"),
        home_season_goals_ratio=format_ratio(x_matchs_data, "home_season_goals_ratio"),
        away_season_goals_ratio=format_ratio(x_matchs_data, "away_season_goals_ratio"),
    )
    return report


def check_team_key(team):
    """
    检查是否以球队名称开始
    """
    if team in CLUB_NAME_MAPPING.keys():
        return True
    return False


def parse_match(matchs, statics_type, **param):
    """
    statics_type: 统计类型
    total_key: 总数key的名称
    goals_ratio_key: 进球数分布比例字段名称
    score_ratio_key: 比分分布比例字段名称
    """
    total_key = param.get("total_key")
    goals_ratio_key = param.get("goals_ratio_key")
    score_ratio_key = param.get("score_ratio_key")
    data = {total_key: len(matchs), goals_ratio_key: dict(), score_ratio_key: dict()}
    for match in matchs:
        if 1 == statics_type:
            tg = match.ftg
            score = "{}-{}".format(match.fthg, match.ftag)
        else:
            tg = match.htg
            score = "{}-{}".format(match.hthg, match.htag)
        # 进球数统计
        if tg not in data[goals_ratio_key].keys():
            data[goals_ratio_key][tg] = 0
        data[goals_ratio_key][tg] += 1
        # 比分统计
        if score not in data[score_ratio_key].keys():
            data[score_ratio_key][score] = 0
        data[score_ratio_key][score] += 1

    return data


def get_match_report(param):
    home_team_ori = param.get("home_team")
    home_team = CLUB_NAME_MAPPING.get(home_team_ori)
    away_team_ori = param.get("away_team")
    away_team = CLUB_NAME_MAPPING.get(away_team_ori)
    number = param.get("number")
    statics_type = param.get("statics_type")
    statics_type_str = "半场进球"
    if 1 == statics_type:
        statics_type_str = "全场进球"

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    # 查询全部比赛
    matchs = nfs.get_last_matchs(
        home_team=home_team, away_team=away_team, number=MAX_MATCHS_NUMBER
    )
    matchs_data = parse_match(
        matchs,
        statics_type=statics_type,
        total_key="total",
        goals_ratio_key="goals_ratio_key",
        score_ratio_key="score_ratio_key",
    )
    # 查询最近number场比赛
    n_match = nfs.get_last_matchs(
        home_team=home_team, away_team=away_team, number=number
    )
    n_matchs_data = parse_match(
        n_match,
        statics_type=statics_type,
        total_key="number",
        goals_ratio_key="goals_match_ratio",
        score_ratio_key="score_match_ratio",
    )
    nfs.close_session()
    nfs.close()
    report = MATCH_REPORT.format(
        statics_type_str=statics_type_str,
        home_team=home_team_ori,
        away_team=away_team_ori,
        total=matchs_data.get("total"),
        goals_total_ratio=format_ratio(matchs_data, "goals_ratio_key"),
        score_total_ratio=format_ratio(matchs_data, "score_ratio_key"),
        number=number,
        goals_match_ratio=format_ratio(n_matchs_data, "goals_match_ratio"),
        score_match_ratio=format_ratio(n_matchs_data, "score_match_ratio"),
    )
    return report
