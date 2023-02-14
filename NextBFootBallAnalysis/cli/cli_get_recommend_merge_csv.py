# -*- coding: utf-8 -*-
# @Time     : 2023/01/16 12:37:16
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_recommend_merge_csv.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_recommend_merge_csv


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-test-recommend",
        description="NextB通过穷举法，生成5大联赛球队最佳组合推荐csv文件。版本号：{}".format(
            NEXTB_FOOTBALL_VERSION
        ),
        epilog="使用方式：nextb-football-test-recommend",
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
    parser.add_argument(
        "-n",
        "--number",
        help="指定最近N场比赛。默认值为：0，表示统计全部比赛",
        type=int,
        dest="number",
        action="store",
        default=0,
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {"csv_name": args.csv_name, "number": args.number}
    try:
        get_recommend_merge_csv(param)
        print("{}文件保存成功。".format(args.csv_name))
    except Exception as e:
        print("出现错误: {}".format(str(e)))
        print("{}文件保存失败。".format(args.csv_name))
