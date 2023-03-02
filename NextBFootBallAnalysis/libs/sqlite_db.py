# -*- coding: utf-8 -*-
# @Time     : 2022/12/30 16:09:17
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : sqlite_db.py
# @Software : Visual Studio Code
# @WeChat   : NextB

import os
from sqlalchemy import (
    create_engine,
    Column,
    String,
    BigInteger,
    or_,
    and_,
    distinct,
    func,
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime, Integer


Base = declarative_base()


class NextbFootballDatas(Base):
    __tablename__ = "nextb_football_datas"
    # sqlite
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    div = Column(String(32))
    season = Column(String(32))
    date_time = Column(DateTime)
    home_team = Column(String(255))
    away_team = Column(String(255))
    fthg = Column(Integer)
    ftag = Column(Integer)
    ftg = Column(Integer)
    ftr = Column(String(32))
    hthg = Column(Integer)
    htag = Column(Integer)
    htg = Column(Integer)
    htr = Column(String(32))


class NextbFootballSqliteDB:
    def __init__(self):
        """
        初始化对象
        """
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.__db_name__ = os.path.join(cur_dir, "NextBFootball.db")
        self.engine = self.init_db_connection(self.__db_name__)
        self.session_maker = None

    @staticmethod
    def init_db_connection(db_name):
        """
        链接数据库
        """
        conn_str = "sqlite:///{db_name}".format(db_name=db_name)
        engine = create_engine(conn_str)
        return engine

    def create_session(self):
        """
        创建数据库链接
        """
        if self.session_maker is None:
            self.session_maker = scoped_session(
                sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
            )

    def close_session(self):
        self.session_maker.close_all()

    def close(self):
        """
        关闭数据库链接
        """
        # self.session_maker.close_all()
        self.engine.dispose()

    # 创建表
    def create_table(self):
        """
        初始化数据表
        """
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            pass

    # 获取当前赛季
    def get_current_season(self):
        """
        获取当前赛季
        """
        data = (
            self.session_maker.query(NextbFootballDatas.season)
            .order_by(NextbFootballDatas.id.desc())
            .limit(1)
        )

        return data[0][0]

    # 构造目标赛季
    def create_season_list(self, current_season, number):
        """
        current_season: 当前赛季
        number: 回溯赛季数目
        """
        seasons = list()
        year = int(current_season.split("-")[0])
        for i in range(-number + 1, 0):
            # 数据最早只能到1993赛季
            if year + i >= 1993:
                seasons.append("{}-{}".format(year + i, year + i + 1))
                seasons.append(current_season)
        return seasons

    def get_team_last_matchs(self, team, number=10):
        """
        获取指定球队最近number场比赛的结果，默认最近10条
        """
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                or_(
                    NextbFootballDatas.home_team == team,
                    NextbFootballDatas.away_team == team,
                )
            )
            .order_by(NextbFootballDatas.id.desc())
            .limit(number)
        )
        if data.count():
            datas = list()
            for d in data:
                datas.append(d)
            datas.reverse()
            return datas
        else:
            return []

    def get_div_goals_group_by(self, div, seasons):
        data = (
            self.session_maker.query(
                NextbFootballDatas.ftg, func.count(NextbFootballDatas.ftg)
            )
            .filter(
                and_(
                    NextbFootballDatas.div == div,
                    NextbFootballDatas.season.in_(seasons),
                )
            )
            .group_by(NextbFootballDatas.ftg)
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []

    def get_team_goals_group_by(self, team, seasons):
        data = (
            self.session_maker.query(
                NextbFootballDatas.ftg, func.count(NextbFootballDatas.ftg)
            )
            .filter(
                and_(
                    or_(
                        NextbFootballDatas.home_team == team,
                        NextbFootballDatas.away_team == team,
                    ),
                    NextbFootballDatas.season.in_(seasons),
                )
            )
            .group_by(NextbFootballDatas.ftg)
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []
        
    def get_home_team_goals_group_by(self, team, seasons):
        data = (
            self.session_maker.query(
                NextbFootballDatas.ftg, func.count(NextbFootballDatas.ftg)
            )
            .filter(
                and_(
                    NextbFootballDatas.home_team == team,
                    NextbFootballDatas.season.in_(seasons),
                )
            )
            .group_by(NextbFootballDatas.ftg)
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []
        
    def get_away_team_goals_group_by(self, team, seasons):
        data = (
            self.session_maker.query(
                NextbFootballDatas.ftg, func.count(NextbFootballDatas.ftg)
            )
            .filter(
                and_(
                    NextbFootballDatas.away_team == team,
                    NextbFootballDatas.season.in_(seasons),
                )
            )
            .group_by(NextbFootballDatas.ftg)
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []

    def get_last_matchs(self, home_team, away_team, number=10):
        """
        获取指定两支球队最近number场比赛的结果，默认最近10条
        """
        teams = [home_team, away_team]
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                and_(
                    NextbFootballDatas.home_team.in_(teams),
                    NextbFootballDatas.away_team.in_(teams),
                )
            )
            .order_by(NextbFootballDatas.id.desc())
            .limit(number)
        )
        if data.count():
            datas = list()
            for d in data:
                datas.append(d)
            datas.reverse()
            return datas
        else:
            return []

    def get_mergeteams_matchs(self, teams, number=10):
        """
        获取指定球队列表最近number场比赛的结果，默认最近10条
        """
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                or_(
                    NextbFootballDatas.home_team.in_(teams),
                    NextbFootballDatas.away_team.in_(teams),
                )
            )
            .order_by(NextbFootballDatas.date_time.desc())
            .limit(number)
        )
        if data.count():
            datas = list()
            for d in data:
                datas.append(d)
            datas.reverse()
            return datas
        else:
            return []

    def get_team_season_matchs(self, teams, season):
        """
        获取指定球队指定赛季的比赛的结果
        """
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                and_(
                    or_(
                        NextbFootballDatas.home_team.in_(teams),
                        NextbFootballDatas.away_team.in_(teams),
                    ),
                    NextbFootballDatas.season.in_(season),
                )
            )
            .order_by(NextbFootballDatas.date_time.asc())
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []

    def get_season_matchs(self, season):
        """
        获取指定赛季的全部比赛的结果
        """
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                NextbFootballDatas.season == season,
            )
            .order_by(NextbFootballDatas.date_time.asc())
            .all()
        )
        if len(data) > 0:
            datas = list()
            for d in data:
                datas.append(d)
            return datas
        else:
            return []

    def get_team_last_season_matchs(self, team, number=5):
        """
        获取指定球队最近number个赛季的比赛结果，默认最近5个赛季
        """
        current_season = self.get_current_season()
        create_season_list = self.create_season_list(current_season, number)
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(
                and_(
                    or_(
                        NextbFootballDatas.home_team == team,
                        NextbFootballDatas.away_team == team,
                    ),
                    NextbFootballDatas.season.in_(create_season_list),
                )
            )
            .order_by(NextbFootballDatas.id.desc())
        )
        if data.count():
            datas = list()
            for d in data:
                datas.append(d)
            datas.reverse()
            return datas
        else:
            return []

    def get_league_last_matchs(self, div, number=10):
        """
        获取指定联赛近number场比赛的结果，默认最近10场
        """
        data = (
            self.session_maker.query(NextbFootballDatas)
            .filter(NextbFootballDatas.div == div)
            .order_by(NextbFootballDatas.id.desc())
            .limit(number)
        )
        if data.count():
            datas = list()
            for d in data:
                datas.append(d)
            datas.reverse()
            return datas
        else:
            return []

    def get_season_teams(self, div, season):
        """
        获取指定赛季的参赛球队列表
        """
        data = (
            self.session_maker.query(distinct(NextbFootballDatas.home_team))
            .filter(
                and_(
                    NextbFootballDatas.div == div,
                    NextbFootballDatas.season == season,
                )
            )
            .all()
        )
        datas = list()
        for d in data:
            datas.append(d[0])
        return datas

    def add_datas(self, datas):
        """
        插入聊天数据
        """
        for data in datas:
            new_data = NextbFootballDatas()
            # 如果插入的数据有问题，则报错退出
            new_data.div = data.get("div")
            new_data.season = data.get("season")
            new_data.date_time = data.get("date_time")
            new_data.home_team = data.get("home_team")
            new_data.away_team = data.get("away_team")
            new_data.fthg = data.get("fthg")
            new_data.ftag = data.get("ftag")
            new_data.ftg = data.get("ftg")
            new_data.ftr = data.get("ftr")
            new_data.hthg = data.get("hthg")
            new_data.htag = data.get("htag")
            new_data.htg = data.get("htg")
            new_data.htr = data.get("htr")
            self.session_maker.add(new_data)
        self.session_maker.commit()
