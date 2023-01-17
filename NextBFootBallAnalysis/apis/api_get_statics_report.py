# -*- coding: utf-8 -*-
# @Time     : 2023/01/12 13:01:40
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : api_get_statics_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


from NextBFootBallAnalysis.libs.constant import STATICS_REPORT
from NextBFootBallAnalysis.libs.common import get_statics_report


def api_get_statics_report(args):
    """
    通过api调用
    """
    # 参数构造
    param = {"league": args.get("league", "")}

    datas = get_statics_report(param)
    reports = list()
    for data in datas:
        name = data[0]
        teams = "{} - {}".format(data[3], data[4])
        match_time = data[2]
        match_half_score = data[5]
        match_full_score = data[6]
        report = STATICS_REPORT.format(
            div=name,
            teams=teams,
            time=match_time,
            h_score=match_half_score,
            f_score=match_full_score,
        )
        reports.append(report)
    return "\n".join(reports)
