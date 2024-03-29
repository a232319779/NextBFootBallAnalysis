# -*- coding: utf-8 -*-
# @Time     : 2023/01/01 15:30:50
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : setup.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import setuptools


def read_version():
    """
    读取打包的版本信息
    """
    with open("./NextBFootBallAnalysis/__init__.py", "r", encoding="utf8") as f:
        for data in f.readlines():
            if data.startswith("NEXTB_FOOTBALL_VERSION"):
                data = data.replace(" ", "")
                version = data.split("=")[-1][1:-1]
                return version
    # 默认返回
    return "1.0.0"


def read_readme():
    """
    读取README信息
    """
    with open("./README.md", "r", encoding="utf8") as f:
        return f.read()


def do_setup(**kwargs):
    try:
        setuptools.setup(**kwargs)
    except (SystemExit, Exception) as e:
        exit(1)


version = read_version()
long_description = read_readme()

do_setup(
    name="NextBFootBallAnalysis",
    version=version,
    author="ddvv",
    author_email="dadavivi512@gmail.com",
    description="NextB的足球比赛数据分析",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a232319779/NextBFootBallAnalysis",
    packages=setuptools.find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "nextb-football-init-db = NextBFootBallAnalysis.cli.cli_init_football_db:run",
            "nextb-football-get-last-matchs = NextBFootBallAnalysis.cli.cli_get_last_matchs:run",
            "nextb-football-get-team = NextBFootBallAnalysis.cli.cli_get_team:run",
            "nextb-football-get-match = NextBFootBallAnalysis.cli.cli_get_match:run",
            "nextb-football-get-recommend = NextBFootBallAnalysis.cli.cli_get_recommend:run",
            "nextb-football-simulation = NextBFootBallAnalysis.cli.cli_simulation:run",
            "nextb-football-get-markdown = NextBFootBallAnalysis.cli.cli_get_markdown:run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords=[],
    license="MIT",
    include_package_data=True,
    install_requires=[
        "sqlalchemy==1.4.31",
        "prettytable==3.6.0",
        "tqdm==4.62.3",
        "python-dateutil",
    ],
)
