# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 10:09:55
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : constant.py
# @Software : Visual Studio Code
# @WeChat   : NextB

# 每支球队每个赛季踢38场比赛,最大假设踢100年
MAX_MATCHS_NUMBER = 38 * 100
# 每个赛季联赛最大场次，20支球队，每支球队每年踢38场，每场比赛2支球队，最大假设有100年的数据
MAX_LEAGUE_MATCHS_NUMBER = 20 * MAX_MATCHS_NUMBER / 2
# 默认最近场次
DEFAULT_MATCHS_NUMBER = 10
# 统计类型，0：半场，1：全场
STATICS_TYPE_HALF = 0
STATICS_TYPE_FULL = 1
# 统计数据类型
STATICS_DATA_TYPE = {
    "all": MAX_MATCHS_NUMBER,
    "10": 10,
    "20": 20,
    "40": 40,
    "50": 50,
    "80": 80
}

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

STATICS_REPORT = """{div}最后一场比赛信息: 
\t比赛双方: {teams}
\t比赛时间: {time}
\t半场比分: {h_score}
\t全场比分: {f_score}
"""

RECOMMEND_REPORT = """联赛名称: {div}
基于历史比赛结果推荐球队如下:
{data}
基于近{number}轮比赛结果推荐球队如下:
{number_data}
"""

# 联赛名称映射表
LEAGUES_MAPPING = {"英超": "E0", "意甲": "I1", "西甲": "SP1", "德甲": "D1", "法甲": "F1"}

# 联赛参赛球队数量
LEAGUE_TEAMS_NUMBER = {
    "E0": 20,
    "I1": 20,
    "SP1": 20,
    "D1": 18,
    "F1": 20,
}

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
    "18": "2018",
    "19": "2019",
    "20": "2020",
    "21": "2021",
    "22": "2022",
}

CLUB_NAME_MAPPING = {
    # 英超
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
    # 意甲
    "安科纳": "Ancona",
    "阿斯科利": "Ascoli",
    "亚特兰大": "Atalanta",
    "巴里": "Bari",
    "贝内文托": "Benevento",
    "博洛尼亚": "Bologna",
    "布雷西亚": "Brescia",
    "卡利亚里": "Cagliari",
    "卡尔皮": "Carpi",
    "卡塔尼亚": "Catania",
    "切塞纳": "Cesena",
    "切沃": "Chievo",
    "科莫": "Como",
    "克雷莫纳": "Cremonese",
    "克罗托内": "Crotone",
    "恩波利": "Empoli",
    "佛罗伦萨": "Fiorentina",
    "霍治亚": "Foggia",
    "弗罗西诺内": "Frosinone",
    "热那亚": "Genoa",
    "国米": "Inter",
    "尤文图斯": "Juventus",
    "拉齐奥": "Lazio",
    "莱切": "Lecce",
    "利沃诺": "Livorno",
    "梅西纳": "Messina",
    "米兰": "Milan",
    "摩德纳": "Modena",
    "蒙扎": "Monza",
    "那不勒斯": "Napoli",
    "诺瓦拉": "Novara",
    "帕多瓦": "Padova",
    "巴勒莫": "Palermo",
    "帕尔马": "Parma",
    "佩鲁贾": "Perugia",
    "佩斯卡拉": "Pescara",
    "皮亚琴察": "Piacenza",
    "雷吉亚纳": "Reggiana",
    "雷吉纳": "Reggina",
    "罗马": "Roma",
    "萨勒尼塔纳": "Salernitana",
    "桑普": "Sampdoria",
    "萨索洛": "Sassuolo",
    "锡耶纳": "Siena",
    "斯帕尔": "Spal",
    "斯佩齐亚": "Spezia",
    "都灵": "Torino",
    "特雷维索": "Treviso",
    "乌迪内斯": "Udinese",
    "威尼斯": "Venezia",
    "维罗纳": "Verona",
    "维琴察": "Vicenza",
    # 西甲
    "阿拉维斯": "Alaves",
    "阿尔瓦塞特": "Albacete",
    "阿尔梅里亚": "Almeria",
    "毕尔巴鄂": "Ath Bilbao",
    "马德里竞技": "Ath Madrid",
    "巴塞罗那": "Barcelona",
    "贝蒂斯": "Betis",
    "加的斯": "Cadiz",
    "塞尔塔": "Celta",
    "孔波斯特拉": "Compostela",
    "科尔多瓦": "Cordoba",
    "埃瓦尔": "Eibar",
    "埃尔切": "Elche",
    "西班牙人": "Espanol",
    "埃斯特雷马杜拉": "Extremadura",
    "赫塔费": "Getafe",
    "塔拉格纳": "Gimnastic",
    "赫罗纳": "Girona",
    "格拉纳达": "Granada",
    "大力神": "Hercules",
    "韦斯卡": "Huesca",
    "拉科鲁尼亚": "La Coruna",
    "拉斯帕尔马斯": "Las Palmas",
    "莱加内斯": "Leganes",
    "列雷达": "Lerida",
    "莱万特": "Levante",
    "洛格朗尼斯": "Logrones",
    "马拉加": "Malaga",
    "马洛卡": "Mallorca",
    "美利达": "Merida",
    "穆尔西亚": "Murcia",
    "努曼西亚": "Numancia",
    "奥萨苏纳": "Osasuna",
    "奥维耶多": "Oviedo",
    "皇家马德里": "Real Madrid",
    "维尔瓦": "Recreativo",
    "萨拉曼卡": "Salamanca",
    "桑坦德": "Santander",
    "塞维利亚": "Sevilla",
    "皇家社会": "Sociedad",
    "希洪竞技": "Sp Gijon",
    "特内里费": "Tenerife",
    "瓦伦西亚": "Valencia",
    "巴拉多利德": "Valladolid",
    "巴列卡诺": "Vallecano",
    "比利亚雷亚尔": "Villarreal",
    "赫雷斯": "Xerez",
    "萨拉戈萨": "Zaragoza",
    # 德甲
    "亚琛": "Aachen",
    "奧格斯堡": "Augsburg",
    "拜仁慕尼黑": "Bayern Munich",
    "比勒费尔德": "Bielefeld",
    "波鸿": "Bochum",
    "布伦瑞克": "Braunschweig",
    "科特布斯": "Cottbus",
    "达姆施塔特": "Darmstadt",
    "多特蒙德": "Dortmund",
    "德累斯顿": "Dresden",
    "杜伊斯堡": "Duisburg",
    "杜塞尔多夫": "Dusseldorf",
    "法兰克福": "Ein Frankfurt",
    "科隆": "FC Koln",
    "杜塞尔多夫": "Fortuna Dusseldorf",
    "弗莱堡": "Freiburg",
    "菲尔特": "Greuther Furth",
    "汉堡": "Hamburg",
    "汉诺威": "Hannover",
    "汉莎罗斯托克": "Hansa Rostock",
    "柏林赫塔": "Hertha",
    "霍芬海姆": "Hoffenheim",
    "因戈尔施塔特": "Ingolstadt",
    "凯泽斯劳滕": "Kaiserslautern",
    "卡尔斯鲁厄": "Karlsruhe",
    "莱比锡": "Leipzig",
    "勒沃库森": "Leverkusen",
    "门兴格莱德巴赫": "M'gladbach",
    "美因兹": "Mainz",
    "慕尼黑1860": "Munich 1860",
    "纽伦堡": "Nurnberg",
    "帕德博恩": "Paderborn",
    "RB莱比锡": "RB Leipzig",
    "沙尔克04": "Schalke 04",
    "圣保利": "St Pauli",
    "斯图加特": "Stuttgart",
    "乌丁根": "Uerdingen",
    "乌尔姆": "Ulm",
    "柏林联合": "Union Berlin",
    "安达赫治": "Unterhaching",
    "波鸿2": "Wattenscheid",
    "不来梅": "Werder Bremen",
    "沃尔夫斯堡": "Wolfsburg",
    # 法甲
    "阿雅克肖": "Ajaccio",
    "阿些斯奥": "Ajaccio GFCO",
    "亚眠": "Amiens",
    "昂热": "Angers",
    "阿尔勒": "Arles",
    "欧塞尔": "Auxerre",
    "巴斯蒂亚": "Bastia",
    "波尔多": "Bordeaux",
    "布洛涅": "Boulogne",
    "布雷斯特": "Brest",
    "卡昂": "Caen",
    "戛纳": "Cannes",
    "沙托鲁": "Chateauroux",
    "克莱蒙": "Clermont",
    "第戎": "Dijon",
    "伊维安": "Evian Thonon Gaillard",
    "格勒诺布尔": "Grenoble",
    "格尼翁": "Gueugnon",
    "甘冈": "Guingamp",
    "伊斯特尔": "Istres",
    "勒阿弗尔": "Le Havre",
    "勒芒": "Le Mans",
    "朗斯": "Lens",
    "里尔": "Lille",
    "洛里昂": "Lorient",
    "里昂": "Lyon",
    "马赛": "Marseille",
    "玛蒂格斯": "Martigues",
    "梅斯": "Metz",
    "摩纳哥": "Monaco",
    "蒙彼利埃": "Montpellier",
    "南希": "Nancy",
    "南特": "Nantes",
    "尼斯": "Nice",
    "尼姆": "Nimes",
    "巴黎圣日耳曼": "Paris SG",
    "兰斯": "Reims",
    "雷恩": "Rennes",
    "色当": "Sedan",
    "索肖": "Sochaux",
    "圣埃蒂安": "St Etienne",
    "斯特拉斯堡": "Strasbourg",
    "图卢兹": "Toulouse",
    "特鲁瓦": "Troyes",
    "瓦朗谢讷": "Valenciennes",
}
