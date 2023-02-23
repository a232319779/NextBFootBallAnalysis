# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:10:29
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : common.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import os
import sys
import datetime
import multiprocessing
from tqdm import tqdm
from collections import Counter
from statistics import mean, median, median_low, median_high
from dateutil.relativedelta import relativedelta
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB
from NextBFootBallAnalysis.libs.constant import (
    YEARS_MAPPING,
    CLUB_NAME_MAPPING,
    MAX_MATCHS_NUMBER,
    DEFAULT_MATCHS_NUMBER,
    LEAGUES_MAPPING,
    STATICS_TYPE_HALF,
    STATICS_TYPE_FULL,
    STATICS_DATA_TYPE,
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

    dist_datas = {STATICS_TYPE_HALF: dict(), STATICS_TYPE_FULL: dict()}
    # 用于动态记录场次间隔变化
    goals_dist_tmp = {STATICS_TYPE_HALF: dict(), STATICS_TYPE_FULL: dict()}
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
    statics_type = {STATICS_TYPE_HALF: "半场进球", STATICS_TYPE_FULL: "全场进球"}
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


def parse_csv_merge_recommend_data(datas):
    recommend_list = list()
    team = datas.get("team")
    history_total = datas.get("total")
    recommend_data = datas.get("recommend_data", [])
    data = recommend_data[0]
    for key, value in data.items():
        if max(value) > 15:
            continue
        tmp_list = list()
        # 球队名称,历史场次,进球数,最大,1/4位,1/2位,3/4位,平均
        tmp_list.append(team)
        tmp_list.append(str(history_total))
        tmp_list.append(str(key))
        tmp_list.append(str(max(value)))
        tmp_list.append(str(median_low(value)))
        tmp_list.append(str(median(value)))
        tmp_list.append(str(median_high(value)))
        tmp_list.append("%.1f" % mean(value))
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
            for sdt, sdt_value in STATICS_DATA_TYPE.items():
                recommend_data = csv_recommend_data(team_sql_data[-sdt_value:])
                team_recommend_data = {
                    "div": name,
                    "team": CLUB_NAME_MAPPING_TRANSFER.get(ct, ct),
                    "total": total,
                    "data_type": "{}".format(sdt),
                    "recommend_data": recommend_data,
                }
                p = parse_csv_recommend_data(team_recommend_data)
                datas.extend(p)
    nfs.close_session()
    nfs.close()
    headers = "联赛名称,球队名称,统计类型,历史场次,比赛场次,进球数,最大,1/4位,1/2位,3/4位,平均,占比1,占比2,占比3"
    with open(csv_name, "w", encoding="utf8") as f:
        f.write(headers + "\n")
        f.write("\n".join(datas))


def process_merge_data(epl_teams, others_teams, number):
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
        for i1_team in tqdm(
            others_teams["I1"],
            unit="team",
            desc="意甲",
            position=1,
            leave=False,
        ):
            for sp1_team in tqdm(
                others_teams["SP1"],
                unit="team",
                desc="西甲",
                position=2,
                leave=False,
            ):
                for f1_team in tqdm(
                    others_teams["F1"],
                    unit="team",
                    desc="法甲",
                    position=3,
                    leave=False,
                ):
                    for d1_team in tqdm(
                        others_teams["D1"],
                        unit="team",
                        desc="德甲",
                        position=4,
                        leave=False,
                    ):
                        merge_teamd = [e0_team, i1_team, sp1_team, d1_team, f1_team]
                        team_sql_data = nfs.get_mergeteams_matchs(
                            merge_teamd, number=number
                        )
                        total = len(team_sql_data)
                        recommend_data = csv_recommend_data(team_sql_data)
                        team_names = [
                            CLUB_NAME_MAPPING_TRANSFER.get(ct, ct) for ct in merge_teamd
                        ]
                        team_recommend_data = {
                            "team": "|".join(team_names),
                            "total": total,
                            "recommend_data": recommend_data,
                        }
                        p = parse_csv_merge_recommend_data(team_recommend_data)
                        datas.extend(p)
    return datas


def get_recommend_merge_csv(param):
    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    try:
        from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
    except:
        sys.exit(0)
    csv_name = param.get("csv_name")
    number = param.get("number", 0)
    number = number if number != 0 else MAX_MATCHS_NUMBER * 5

    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    datas = list()
    current_teams = dict()
    # 获取当前赛季各大联赛参赛球队列表
    for _, div in LEAGUES_MAPPING.items():
        # 查询当前赛季
        last_match = nfs.get_league_last_matchs(div=div, number=1)
        # 未查询到数据
        if not last_match:
            continue
        # 查询本赛季参赛球队列表
        current_teams[div] = nfs.get_season_teams(div, last_match[-1].season)
    nfs.close_session()
    nfs.close()
    max_workers = 10
    e0_teams = current_teams["E0"]
    datas = list()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        all_task = [
            executor.submit(
                process_merge_data, e0_teams[k : k + 2], current_teams, number
            )
            for k in range(0, len(e0_teams), 2)
        ]
        wait(all_task, return_when=ALL_COMPLETED)
        for task in all_task:
            result = task.result()
            datas.extend(result)

    headers = "球队名称,历史场次,进球数,最大,1/4位,1/2位,3/4位,平均"
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
        tmp.append(m.date_time.strftime("%Y/%m/%d %H:%M"))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.home_team, m.home_team))
        tmp.append(CLUB_NAME_MAPPING_TRANSFER.get(m.away_team, m.away_team))
        tmp.append("{}-{}".format(m.hthg, m.htag))
        tmp.append("{}-{}".format(m.fthg, m.ftag))
        datas.append(tmp)
    datas.reverse()
    return datas
