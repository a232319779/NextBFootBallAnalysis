# -*- coding: utf-8 -*-
# @Time     : 2023/01/03 16:04:33
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_init_football_db.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import argparse
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_file_list, parse_data
from NextBFootBallAnalysis.libs.sqlite_db import NextbFootballSqliteDB

def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-init-db",
        description="NextB初始化football数据库。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-init-db -d $csv_dir",
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="设置csv文件目录",
        type=str,
        dest="csv_dir",
        action="store",
        default="",
    )

    args = parser.parse_args()

    return args

def init_football_db(args):
    file_dir = args.csv_dir
    file_paths = get_file_list(file_dir)
    datas = list()
    nfs = NextbFootballSqliteDB()
    nfs.create_session()
    nfs.create_table()
    for file_name in file_paths:
        data = parse_data(file_name)
        if data:
            datas.extend(data)
    nfs.add_datas(datas)
    nfs.close_session()
    nfs.close()
    print("初始化完成.数据库保存路径: {}".format(nfs.__db_name__))


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    init_football_db(args)
