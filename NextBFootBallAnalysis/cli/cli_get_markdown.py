# -*- coding: utf-8 -*-
# @Time     : 2023/03/03 15:06:10
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_markdown.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_markdown


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-markdown",
        description="NextB获取指定两支球队的分析报告。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-markdown -t 曼联 阿森纳",
    )
    parser.add_argument(
        "-t",
        "--teams",
        help="指定球队名称。指定2支球队名称，超过2支则取前2支球队。默认值：['切尔西', '曼联']",
        nargs="+",
        dest="teams",
        action="store",
        default=["切尔西", "曼联"],
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "teams": args.teams,
    }
    get_markdown(param)
