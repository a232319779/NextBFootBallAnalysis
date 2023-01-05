# 足球数据分析

**注意：github源码中不包含数据库文件，`pip`包中包含数据库文件**

## 一、数据

|联赛|数据录入|开始赛季|数据更新时间|
|----|----|----|----|
|英超|✔|1993-1994|2023-01-01|
|意甲||||
|德甲||||
|西甲||||
|法甲||||

## 二、命令行

|功能点|说明|使用示例|
|----|----|----|
|nextb-football-init-db|NextB初始化football数据库|`nextb-football-init-db -d $csv_dir`|
|nextb-football-update-db|NextB更新football数据库|`nextb-football-update-db -f $csv_file -n $update_number`|
|nextb-football-team-report|NextB获取指定球队的分析报告，报告格式参考[球队分析报告](#31-球队分析报告格式如下)|`nextb-football-team-report -n 热刺`|
|nextb-football-match-report|NextB获取指定两支球队的比赛分析报告，报告格式参考[比赛分析报告](#32-比赛分析报告格式)|`nextb-football-match-report -h 切尔西 -a 曼城`|
|||||

## 三、分析结果

### 3.1 球队分析报告格式

```python
TEAM_REPORT = """球队名称：{team}

统计类型: {statics_type_str}
历史比赛场次：{total}
历史进球场次及占比：{goals_total_ratio}
主场进球场次及占比：{home_goals_total_ratio}
客场进球场次及占比：{away_goals_total_ratio}
近{number}场比赛进球场次及占比：{match_goals_ratio}
近{home_number}场比赛主场进球场次及占比：{home_match_goals_rartio}
近{away_number}场比赛客场进球场次及占比：{away_match_goals_ratio}
近{xnumber}个赛季场次: {season_total}
近{xnumber}个赛季进球场次及占比：{season_goals_ratio}
近{xnumber}个赛季主场进球场次及占比：{home_season_goals_ratio}
近{xnumber}个赛季客场进球场次及占比：{away_season_goals_ratio}
"""
```

### 3.2 比赛分析报告格式

```python
match_report = """
主队名称: {}
客队名称: {}
双方历史交手场次：{}
双方历史进球场次及占比：{}, {}
近$X个赛季交手进球场次及占比：{}
近$N场比赛进球场次及占比：{}
"""
```

## 四、据库存储格式

|字段名称|字段类型|字段说明|
|----|----|----|
|id|int|记录ID, 主键, 自增|
|div|str|联赛名称, E0: 英超|
|season|str|赛季, 如: 2022-2023|
|date_time|datetime|比赛时间|
|home_team|str|主队名称|
|away_team|str|客队名称|
|fthg|int|全场主队进球|
|ftag|int|全场客队进球|
|ftg|int|全场进球数|
|ftr|str|全场比赛结果, H: 主队胜, A: 客队胜, D: 平局|
|hthg|int|半场主队进球, 缺省值为-1|
|htag|int|半场客队进球, 缺省值为-1|
|htg|int|半场进球数, 缺省值为-1|
|htr|str|半场比赛结果, H: 主队胜, A: 客队胜, D: 平局|

## 五、微信小程序

### 5.1 发送球队名称，获取球队分析结果

发送命令格式，用`空格`分隔：`球队名称 [可选,默认最近10场]最近比赛场次 [可选,默认最近5个赛季]最近赛季数量 [可选,默认统计半场进球]0`

示例命令如下：

```
切尔西            # 统计切尔西最近10场比赛、最近5个赛季比赛的半场进球数
切尔西 15         # 统计切尔西最近15场比赛、最近5个赛季比赛的半场进球数
切尔西 15 3       # 统计切尔西最近15场比赛、最近3个赛季比赛的半场进球数
切尔西 12 4 1     # 统计切尔西最近12场比赛、最近4个赛季比赛的全场进球数
```

![](https://github.com/a232319779/NextBFootBallAnalysis/pictures/team.png)

### 5.2 发送比赛双方球队名称，获取比赛分析结果

发送命令格式，用`空格`分隔：`主队名称 客队名称 [可选,默认最近10场]最近比赛场次 [可选,默认统计半场进球]0`

示例命令如下：

```
切尔西 曼城             # 统计切尔西和曼城最近10场比赛的半场进球数
切尔西 曼城 15          # 统计切尔西和曼城最近15场比赛的半场进球数
切尔西 曼城 12 1        # 统计切尔西和曼城最近12场比赛的全场进球数
```

![](https://github.com/a232319779/NextBFootBallAnalysis/pictures/match.png)

## 六、小程序二维码

微信扫描二维码，体验小程序

![](https://github.com/a232319779/NextBFootBallAnalysis/pictures/wechat_mini.png)
