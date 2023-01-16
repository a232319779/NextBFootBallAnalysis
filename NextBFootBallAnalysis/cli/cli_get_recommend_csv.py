# -*- coding: utf-8 -*-
# @Time     : 2023/01/16 12:37:16
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_recommend_csv.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_recommend_csv


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-recommend-csv",
        description="NextB生成球队推荐csv文件。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-recommend-report -n $number",
    )
    parser.add_argument(
        "-c",
        "--csv_name",
        help="指定保存结果的csv文件名称,默认保存为: ./NextBFootBallRecommend.csv.",
        type=str,
        dest="csv_name",
        action="store",
        default="NextBFootBallRecommend.csv",
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "csv_name": args.csv_name
    }
    try:
        get_recommend_csv(param)
        print("{}文件保存成功。".format(args.csv_name))
    except Exception as e:
        print("出现错误: {}".format(str(e)))
        print("{}文件保存失败。".format(args.csv_name))
