# -*- coding: utf-8 -*-
# @Time     : 2023/01/04 12:46:49
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : api_get_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB

from NextBFootBallAnalysis.libs.common import get_report

def api_get_report(args):
    """
    通过api调用
    """
    # 参数构造
    param = {
        "team": args.get("team", "阿森纳"),
        "number": args.get("number", 10),
        "xnumber": args.get("xumber", 5),
        "statics_type": args.get("statics_type", 0)
    }
    return get_report(param)