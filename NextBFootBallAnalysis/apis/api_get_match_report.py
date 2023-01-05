# -*- coding: utf-8 -*-
# @Time     : 2023/01/04 22:48:35
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : api_get_match_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


from NextBFootBallAnalysis.libs.common import get_match_report

def api_get_match_report(args):
    """
    通过api调用
    """
    home_team = args.get("home_team", "")
    away_team = args.get("away_team", "")
    if home_team == away_team == "":
        return "交战双方不能为空。"
    # 参数构造
    param = {
        "home_team": home_team,
        "away_team": away_team,
        "number": args.get("number", 10),
        "statics_type": args.get("statics_type", 0),
    }
    return get_match_report(param)