# -*- coding: utf-8 -*-
# @Time     : 2023/01/12 16:41:20
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : api_get_recommend_report.py
# @Software : Visual Studio Code
# @WeChat   : NextB


from NextBFootBallAnalysis.libs.common import get_recommend_report


def api_get_recommend_report(args):
    """
    通过api调用
    """
    # 参数构造
    param = {
        "number": args.get("number", 10),
        "statics_type": args.get("statics_type", 0),
    }
    return get_recommend_report(param)
