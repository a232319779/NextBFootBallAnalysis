# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:09:55
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : constant.py
# @Software : Visual Studio Code
# @WeChat   : NextB

# 每支球队每个赛季踢38场比赛,最大假设踢100年
MAX_MATCHS_NUMBER = 38 * 100

TEAM_REPORT = """球队名称：{team}

统计类型: {statics_type_str}
近{number}场比赛进球场次及占比：{match_goals_ratio}
近{home_number}场比赛主场进球场次及占比：{home_match_goals_rartio}
近{away_number}场比赛客场进球场次及占比：{away_match_goals_ratio}
历史比赛场次：{total}
历史进球场次及占比：{goals_total_ratio}
主场进球场次及占比：{home_goals_total_ratio}
客场进球场次及占比：{away_goals_total_ratio}
历史进球场次间隔: {goals_dist}
近{xnumber}个赛季场次: {season_total}
近{xnumber}个赛季进球场次及占比：{season_goals_ratio}
近{xnumber}个赛季主场进球场次及占比：{home_season_goals_ratio}
近{xnumber}个赛季客场进球场次及占比：{away_season_goals_ratio}
近{xnumber}个赛季进球场次间隔: {xnumber_goals_dist}
"""

MATCH_REPORT = """交战双方: {home_team} vs {away_team}
统计类型: {statics_type_str}
双方历史交手场次：{total}
双方历史进球场次及占比：{goals_total_ratio}
双方历史比分场次及占比：{score_total_ratio}
双方近{number}场比赛进球场次及占比：{goals_match_ratio}
双方近{number}场比赛比分场次及占比：{score_match_ratio}
"""

YEARS_MAPPING = {
    "93": "1993",
    "94": "1994",
    "95": "1995",
    "96": "1996",
    "97": "1997",
    "98": "1998",
    "99": "1999",
    "00": "2000",
    "01": "2001",
    "02": "2002",
    "03": "2003",
    "04": "2004",
    "05": "2005",
    "06": "2006",
    "07": "2007",
    "08": "2008",
    "09": "2009",
    "10": "2010",
    "11": "2011",
    "12": "2012",
    "13": "2013",
    "14": "2014",
    "15": "2015",
    "16": "2016",
    "17": "2017",
}

CLUB_NAME_MAPPING = {
    "切尔西": "Chelsea",
    "埃弗顿": "Everton",
    "利物浦": "Liverpool",
    "谢周三": "Sheffield Weds",
    "利兹联": "Leeds",
    "阿森纳": "Arsenal",
    "曼联": "Man United",
    "西汉姆": "West Ham",
    "汉诺丁森林": "Nott'm Forest",
    "热刺": "Tottenham",
    "维拉": "Aston Villa",
    "考文垂": "Coventry",
    "纽卡斯尔": "Newcastle",
    "布莱克本": "Blackburn",
    "博尔顿": "Bolton",
    "曼城": "Man City",
    "米德尔斯堡": "Middlesbrough",
    "南安普敦": "Southampton",
    "女王公园巡游者": "QPR",
    "温布尔登": "Wimbledon",
    "桑德兰": "Sunderland",
    "莱斯特城": "Leicester",
    "德比郡": "Derby",
    "水晶宫": "Crystal Palace",
    "巴恩斯利": "Barnsley",
    "查尔顿": "Charlton",
    "布拉德福德": "Bradford",
    "沃特福德": "Watford",
    "伊普斯维奇": "Ipswich",
    "富勒姆": "Fulham",
    "西布朗": "West Brom",
    "伯明翰": "Birmingham",
    "朴次茅斯": "Portsmouth",
    "狼队": "Wolves",
    "诺维奇": "Norwich",
    "维冈": "Wigan",
    "谢菲尔德联": "Sheffield United",
    "雷丁": "Reading",
    "斯托克城": "Stoke",
    "赫尔城": "Hull",
    "伯恩利": "Burnley",
    "布莱克浦": "Blackpool",
    "斯旺西": "Swansea",
    "卡迪夫城": "Cardiff",
    "伯恩茅斯": "Bournemouth",
    "布莱顿": "Brighton",
    "哈德斯菲尔德": "Huddersfield",
    "布伦特福德": "Brentford",
    "Chelsea": "Chelsea",
    "Everton": "Everton",
    "Liverpool": "Liverpool",
    "Sheffield Weds": "Sheffield Weds",
    "Leeds": "Leeds",
    "Arsenal": "Arsenal",
    "Man United": "Man United",
    "West Ham": "West Ham",
    "Nott'm Forest": "Nott'm Forest",
    "Tottenham": "Tottenham",
    "Aston Villa": "Aston Villa",
    "Coventry": "Coventry",
    "Newcastle": "Newcastle",
    "Blackburn": "Blackburn",
    "Bolton": "Bolton",
    "Man City": "Man City",
    "Middlesbrough": "Middlesbrough",
    "Southampton": "Southampton",
    "QPR": "QPR",
    "Wimbledon": "Wimbledon",
    "Sunderland": "Sunderland",
    "Leicester": "Leicester",
    "Derby": "Derby",
    "Crystal Palace": "Crystal Palace",
    "Barnsley": "Barnsley",
    "Charlton": "Charlton",
    "Bradford": "Bradford",
    "Watford": "Watford",
    "Ipswich": "Ipswich",
    "Fulham": "Fulham",
    "West Brom": "West Brom",
    "Birmingham": "Birmingham",
    "Portsmouth": "Portsmouth",
    "Wolves": "Wolves",
    "Norwich": "Norwich",
    "Wigan": "Wigan",
    "Sheffield United": "Sheffield United",
    "Reading": "Reading",
    "Stoke": "Stoke",
    "Hull": "Hull",
    "Burnley": "Burnley",
    "Blackpool": "Blackpool",
    "Swansea": "Swansea",
    "Cardiff": "Cardiff",
    "Bournemouth": "Bournemouth",
    "Brighton": "Brighton",
    "Huddersfield": "Huddersfield",
    "Brentford": "Brentford",
}
