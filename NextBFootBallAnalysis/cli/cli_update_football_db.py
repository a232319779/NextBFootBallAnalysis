# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 16:40:28
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_update_football_db.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import parse_data
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB

def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-update-db",
        description="NextB更新football数据库。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-update-db -f $csv_file -n $update_number",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="设置csv文件路径",
        type=str,
        dest="csv_file",
        action="store",
        default="",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="设置更新条数,默认更新最近10条",
        type=int,
        dest="number",
        action="store",
        default=10,
    )

    args = parser.parse_args()

    return args

def update_football_db(args):
    file_name = args.csv_file
    number = args.number
    datas = list()
    data = parse_data(file_name, number)
    if data:
        datas.extend(data)
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    nfs.add_datas(datas)
    nfs.close_session()
    nfs.close()


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    update_football_db(args)
