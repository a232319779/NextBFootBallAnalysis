# -*- coding: utf-8 -*-
# @Time     : 2023/01/12 13:01:40
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : api_get_statics_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


from NextBFootBallAnalysis.libs.common import get_statics_report


def api_get_statics_report(args):
    """
    通过api调用
    """
    # 参数构造
    param = {"league": args.get("league", "")}
    return get_statics_report(param)