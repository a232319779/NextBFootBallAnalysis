# -*- coding: utf-8 -*-
# @Time     : 2023/01/16 12:37:16
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : cli_get_recommend.py
# @Software : Visual Studio Code
# @WeChat   : NextB


import datetime
import argparse
from prettytable import PrettyTable
from NextBFootBallAnalysis import NEXTB_FOOTBALL_VERSION
from NextBFootBallAnalysis.libs.common import get_recommend


def parse_cmd():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="nextb-football-recommend",
        description="NextB生成球队推荐结果。版本号：{}".format(NEXTB_FOOTBALL_VERSION),
        epilog="使用方式：nextb-football-recommend",
    )
    parser.add_argument(
        "-s",
        "--season",
        help="指定赛季名称。默认为2022-2023赛季，赛季格式如：2022-2023。",
        type=str,
        dest="season",
        action="store",
        default="2022-2023",
    )
    parser.add_argument(
        "-g",
        "--goals",
        help="指定进球数量，可选值包括[0,1,2,3,4,5,6,7]，自动忽略其他值默认为：2球",
        type=int,
        dest="goals",
        action="store",
        default=2,
    )
    parser.add_argument(
        "-st",
        "--statics_type",
        help="指定进球统计类型,可选值包括[0: 半场, 1: 全场],默认值为: 1,统计全场进球数.",
        type=int,
        dest="statics_type",
        action="store",
        default=1,
    )

    args = parser.parse_args()

    return args


def run():
    """
    CLI命令行入口
    """
    args = parse_cmd()
    param = {
        "season": args.season,
        "goals": args.goals,
        "statics_type": args.statics_type,
    }

    datas = get_recommend(param)
    x = PrettyTable()
    x.field_names = [
        "联赛名称",
        "半全场",
        "球队名称",
        "{}球未出现场次".format(args.goals),
        "联赛{}球占比".format(args.goals),
        "比赛场次",
        "球队{}球占比".format(args.goals),
        "主场{}球占比".format(args.goals),
        "客场{}球占比".format(args.goals),
        "本赛{}球占比".format(args.goals),
        "占比方差",
    ]
    for _, data in datas.items():
        x.add_rows(data)
    print(
        "说明：\n联赛N球占比：基于历史数据计算出的该联赛进N球的占比\n球队N球占比：基于历史数据计算出的该球队进N球的占比\n主场N球占比：基于近3个赛季该球队主场进N球的占比"
    )
    print(x)

    # 将结果转为str，输出到csv文件
    csv_data = list()
    for _, data in datas.items():
        for d in data:
            csv_data.append("{},{},{},{},{},{},{},{},{},{},{}".format(*d))
    # 保存推荐结果到csv文件，方便后续人工查看
    st = "全场"
    if args.statics_type == 0:
        st = "半场"
    csv_file_name = "五大联赛-{}-{}-{}球.csv".format(
        datetime.datetime.now().strftime("%Y-%m-%d"), st, args.goals
    )
    with open(csv_file_name, "w", encoding="utf8") as f:
        f.write(",".join(x.field_names))
        f.write("\n")
        f.write("\n".join(csv_data))
