# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:10:29
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : common.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import os
import datetime
from collections import Counter
from statistics import mean, median, median_low, median_high
from dateutil.relativedelta import relativedelta
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from NextBFootBallAnalysis.libs.constant import (
    YEARS_MAPPING,
    CLUB_NAME_MAPPING,
    TEAM_REPORT,
    MATCH_REPORT,
    STATICS_REPORT,
    RECOMMEND_REPORT,
    MAX_MATCHS_NUMBER,
    DEFAULT_MATCHS_NUMBER,
    MAX_LEAGUE_MATCHS_NUMBER,
    LEAGUES_MAPPING,
    LEAGUE_TEAMS_NUMBER,
    STATICS_TYPE_HALF,
    STATICS_TYPE_FULL,
    STATICS_DATA_TYPE
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
    goals_dist: 进球场次间隔
    """
    team = param.get("team")
    total = param.get("total_key")
    ratio_key = param.get("ratio_key")
    home_ratio_key = param.get("home_ratio_key")
    away_ratio_key = param.get("away_ratio_key")
    goals_dist = param.get("goals_dist")
    data = {
        total: len(matchs),
        ratio_key: dict(),
        home_ratio_key: dict(),
        away_ratio_key: dict(),
        goals_dist: dict(),
    }
    # 用于动态记录场次间隔变化
    goals_dist_tmp = dict()
    for match in matchs:
        if STATICS_TYPE_FULL == statics_type:
            tg = match.ftg
        else:
            tg = match.htg
        # 进球数统计
        if tg not in data[ratio_key].keys():
            data[ratio_key][tg] = 0
        data[ratio_key][tg] += 1
        # 统计进球间隔场次
        if tg != -1:
            if tg in goals_dist_tmp.keys():
                if tg not in data[goals_dist].keys():
                    data[goals_dist][tg] = list()
                data[goals_dist][tg].append(goals_dist_tmp[tg])
            # 老的进球场数间隔+1场
            for a in goals_dist_tmp.keys():
                goals_dist_tmp[a] += 1
            # 新的进球场数间隔清0
            goals_dist_tmp[tg] = 0
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
    team = CLUB_NAME_MAPPING.get(team_ori, team_ori)
    number = param.get("number", DEFAULT_MATCHS_NUMBER)
    xnumber = param.get("xnumber")
    statics_type = param.get("statics_type")
    statics_type_str = "半场进球"
    if STATICS_TYPE_FULL == statics_type:
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
        goals_dist="goals_dist",
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
        goals_dist="goals_dist",
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
        goals_dist="goals_dist",
    )
    nfs.close_session()
    nfs.close()
    home_number = sum(n_matchs_data.get("home_match_goals_rartio").values())
    away_number = sum(n_matchs_data.get("away_match_goals_ratio").values())
    # season_total = sum(x_matchs_data.get("season_goals_ratio").values())
    season_total = x_matchs_data.get("xnumber")
    report = TEAM_REPORT.format(
        team=team_ori,
        statics_type_str=statics_type_str,
        total=matchs_data.get("total"),
        goals_total_ratio=format_ratio(matchs_data, "goals_total_ratio"),
        home_goals_total_ratio=format_ratio(matchs_data, "home_goals_total_ratio"),
        away_goals_total_ratio=format_ratio(matchs_data, "away_goals_total_ratio"),
        goals_dist=format_list(matchs_data, "goals_dist"),
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
        xnumber_goals_dist=format_list(x_matchs_data, "goals_dist"),
    )
    return report


def check_team_key(team):
    """
    检查是否以球队名称开始
    """
    if team in CLUB_NAME_MAPPING.keys() or team in CLUB_NAME_MAPPING.values():
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
        if STATICS_TYPE_FULL == statics_type:
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
    home_team = CLUB_NAME_MAPPING.get(home_team_ori, home_team_ori)
    away_team_ori = param.get("away_team")
    away_team = CLUB_NAME_MAPPING.get(away_team_ori, away_team_ori)
    number = param.get("number", DEFAULT_MATCHS_NUMBER)
    statics_type = param.get("statics_type")
    statics_type_str = "半场进球"
    if STATICS_TYPE_FULL == statics_type:
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


def statics_goals_dist(matchs, current_teams, statics_type):
    """
    统计指定球队的进球间隔场次
    """
    # 按球队保存比赛信息
    teams = dict()
    for match in matchs:
        home_team = match.home_team
        away_team = match.away_team
        if home_team in current_teams:
            if home_team not in teams.keys():
                teams[home_team] = list()
            teams[home_team].append(match)
        if away_team in current_teams:
            if away_team not in teams.keys():
                teams[away_team] = list()
            teams[away_team].append(match)

    datas = dict()
    for team, team_matchs in teams.items():
        # 用于动态记录场次间隔变化
        goals_dist_tmp = dict()
        for match in team_matchs:
            if STATICS_TYPE_FULL == statics_type:
                tg = match.ftg
            else:
                tg = match.htg
            # 统计进球间隔场次
            if tg != -1:
                if tg in goals_dist_tmp.keys():
                    if team not in datas.keys():
                        datas[team] = dict()
                    if tg not in datas[team].keys():
                        datas[team][tg] = list()
                    datas[team][tg].append(goals_dist_tmp[tg])
                # 老的进球场数间隔+1场
                for a in goals_dist_tmp.keys():
                    goals_dist_tmp[a] += 1
                # 新的进球场数间隔清0
                goals_dist_tmp[tg] = 0
    return datas


def recommend_goals_dist(datas, club_name_mapping_transfer):
    """
    获取推荐球队，推荐原则：中位数最小优先、平均数最小次之、最大间隔最小最后
    """
    recommend_list = list()
    for team, data in datas.items():
        for key, value in data.items():
            if key not in [0, 1]:
                continue
            tmp_list = list()
            value_new = sorted(value)
            # 统计进球场次最大间隔
            max_dist = max(value_new)
            # 统计进球场次平均间隔
            mean_dist = "%.1f" % mean(value_new)
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

            tmp_list.append(
                "球队名称:{}".format(club_name_mapping_transfer.get(team, team))
            )
            tmp_list.append("进{}球最大间隔:{}场".format(str(key), max_dist))
            tmp_list.append("进{}球平均间隔:{}场".format(str(key), mean_dist))
            tmp_list.append("进{}球中位数间隔:{}场".format(str(key), median_dist))
            tmp_list.append(
                "进{}球出现场次及占比:{}".format(str(key), ",".join(counter_str_list))
            )
            tmp = [median_dist, mean_dist, max_dist, ",".join(tmp_list)]
            recommend_list.append(tmp)
    recommend_list = sorted(recommend_list, key=lambda a: (a[0], a[1], a[2]))
    out = [a[3] for a in recommend_list[:3]]
    return "\n".join(out)


def get_statics_report(param):
    league = param.get("league")
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    if league:
        if LEAGUES_MAPPING.get(league, None) is None:
            print("输入正确的联赛名称，取值包括：[英超,意甲,西甲,德甲,法甲]")
            exit()
        leagues_mapping = {league: LEAGUES_MAPPING.get(league)}
    else:
        leagues_mapping = LEAGUES_MAPPING
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    reports = list()
    for name, div in leagues_mapping.items():
        # 查询联赛最后一场
        matchs = nfs.get_league_last_matchs(div=div, number=1)
        # 未查询到数据
        if not matchs:
            continue
        m = matchs[0]
        # 填充最后一场比赛的信息
        teams = "{} - {}".format(
            CLUB_NAME_MAPPING_TRANSFER.get(m.home_team, m.home_team),
            CLUB_NAME_MAPPING_TRANSFER.get(m.away_team, m.away_team),
        )
        match_time = m.date_time.strftime("%Y-%m-%d %H:%M")
        match_score = "{}-{}".format(m.fthg, m.ftag)

        report = STATICS_REPORT.format(
            div=name, teams=teams, time=match_time, score=match_score
        )
        reports.append(report)
    nfs.close_session()
    nfs.close()
    return "".join(reports)


def get_recommend_report(param):
    number = param.get("number", DEFAULT_MATCHS_NUMBER)
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )
    statics_type = param.get("statics_type")
    statics_type_str = "半场比分"
    if STATICS_TYPE_FULL == statics_type:
        statics_type_str = "全场比分"

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    reports = list()
    for name, div in LEAGUES_MAPPING.items():
        # 查询联赛全部比赛
        matchs = nfs.get_league_last_matchs(div=div, number=MAX_LEAGUE_MATCHS_NUMBER)
        # 未查询到数据
        if not matchs:
            continue
        # 查询本赛季参赛球队列表
        current_teams = nfs.get_season_teams(div, matchs[-1].season)
        # 计算球队历史场次进球间隔场次
        team_goals_dist = statics_goals_dist(matchs, current_teams, statics_type)
        data = recommend_goals_dist(team_goals_dist, CLUB_NAME_MAPPING_TRANSFER)
        # 获取最近number轮比赛
        last_number_matchs = matchs[-number * LEAGUE_TEAMS_NUMBER.get(div) :]
        # 计算球队最近number轮场次进球间隔场次
        team_number_goals_dist = statics_goals_dist(
            last_number_matchs, current_teams, statics_type
        )
        number_data = recommend_goals_dist(
            team_number_goals_dist, CLUB_NAME_MAPPING_TRANSFER
        )

        report = RECOMMEND_REPORT.format(
            div=name,
            statics_type_str=statics_type_str,
            data=data,
            number=number,
            number_data=number_data,
        )
        reports.append(report)
    nfs.close_session()
    nfs.close()
    return "\n".join(reports)

def csv_recommend_data(team_matchs):
    def parse_data(statics_type):
        if STATICS_TYPE_FULL == statics_type:
            tg = match.ftg
        else:
            tg = match.htg
        # 统计进球间隔场次
        if tg != -1:
            if tg in goals_dist_tmp[statics_type].keys():
                if tg not in dist_datas[statics_type].keys():
                    dist_datas[statics_type][tg] = list()
                dist_datas[statics_type][tg].append(goals_dist_tmp[statics_type][tg])
            # 老的进球场数间隔+1场
            for a in goals_dist_tmp[statics_type].keys():
                goals_dist_tmp[statics_type][a] += 1
            # 新的进球场数间隔清0
            goals_dist_tmp[statics_type][tg] = 0
    dist_datas = {
        STATICS_TYPE_HALF: dict(),
        STATICS_TYPE_FULL: dict()
    }
    # 用于动态记录场次间隔变化
    goals_dist_tmp = {
        STATICS_TYPE_HALF: dict(),
        STATICS_TYPE_FULL: dict()
    }
    for match in team_matchs:
        # 半场进球类型
        parse_data(STATICS_TYPE_HALF)
        # 全场进球类型
        parse_data(STATICS_TYPE_FULL)
        
    return dist_datas

def parse_csv_recommend_data(datas):
    recommend_list = list()
    div = datas.get("div")
    team = datas.get("team")
    history_total = datas.get("total")
    data_type = datas.get("data_type")
    statics_type = {
        STATICS_TYPE_HALF: "半场进球",
        STATICS_TYPE_FULL: "全场进球"
    }
    recommend_data = datas.get("recommend_data", [])
    for st, data in recommend_data.items():
        for key, value in data.items():
            # 统计每个进球场次间隔的占比
            counter_str_list = list()
            counter = Counter(value)
            total = sum(counter.values())
            index = 0
            for a, b in counter.most_common():
                b1 = "%.2f" % (b / total)
                counter_str_list.append("{}|{}".format(str(a), str(b1)))
                index += 1
                # 只看top3的
                if index >= 3:
                    break
            tmp_list = list()
            # 联赛名称,球队名称,统计类型,历史场次,比赛场次,进球数,最大,1/4位,1/2位,3/4位,平均,占比1,占比2,占比3
            tmp_list.append(div)
            tmp_list.append(team)
            tmp_list.append(statics_type.get(st))
            tmp_list.append(str(history_total))
            tmp_list.append(data_type)
            tmp_list.append(str(key))
            tmp_list.append(str(max(value)))
            tmp_list.append(str(median_low(value)))
            tmp_list.append(str(median(value)))
            tmp_list.append(str(median_high(value)))
            tmp_list.append("%.1f" % mean(value))
            tmp_list.extend(counter_str_list)
            recommend_list.append(",".join(tmp_list))
    return recommend_list

def get_recommend_csv(param):
    csv_name = param.get("csv_name")
    # 转换为中文名称
    CLUB_NAME_MAPPING_TRANSFER = dict(
        zip(CLUB_NAME_MAPPING.values(), CLUB_NAME_MAPPING.keys())
    )

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    for name, div in LEAGUES_MAPPING.items():
        # 查询联赛全部比赛
        matchs = nfs.get_league_last_matchs(div=div, number=1)
        # 未查询到数据
        if not matchs:
            continue
        # 查询本赛季参赛球队列表
        current_teams = nfs.get_season_teams(div, matchs[-1].season)
        for ct in current_teams:
            team_sql_data = nfs.get_team_last_matchs(ct, number=MAX_MATCHS_NUMBER)
            total = len(team_sql_data)
            for sdt,sdt_value in STATICS_DATA_TYPE.items():
                recommend_data = csv_recommend_data(team_sql_data[-sdt_value:])
                team_recommend_data = {
                    "div": name,
                    "team": CLUB_NAME_MAPPING_TRANSFER.get(ct, ct),
                    "total": total,
                    "data_type": "{}".format(sdt),
                    "recommend_data": recommend_data
                }
                p = parse_csv_recommend_data(team_recommend_data)
                datas.extend(p)
    nfs.close_session()
    nfs.close()
    headers = "联赛名称,球队名称,统计类型,历史场次,比赛场次,进球数,最大,1/4位,1/2位,3/4位,平均,占比1,占比2,占比3"
    with open(csv_name, "w", encoding="utf8") as f:
        f.write(headers + "\n")
        f.write("\n".join(datas))

def get_team_match(param):
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
        tmp.append(m.date_time.strftime("%Y/%m/%d %H"))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.home_team, m.home_team))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.away_team, m.away_team))
        tmp.append("{}-{}".format(m.hthg, m.htag))
        tmp.append("{}-{}".format(m.fthg, m.ftag))
        datas.append(tmp)
    datas.reverse()
    return datas