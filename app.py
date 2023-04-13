import csv

from flask import Flask, render_template, url_for, redirect, jsonify, request
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts import options
from pyecharts.globals import ThemeType
import pandas as pd
import json
from spider.weibo.DBManager import *

app = Flask(__name__)
"""
DB_URI = "mysql+pymysql://root:0226@127.0.0.1:3306/weibo"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
# 是否追踪数据库修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 是否显示底层执行的SQL语句
app.config["SQLALCHEMY_ECHO"] = True
"""
# 初始化db，关联flask项目
db = DBManager()


# 绘制Top热搜柱状图
def hotSearch_bar(data):
    bar = Bar(init_opts=options.InitOpts(theme=ThemeType.MACARONS, width="1600px", height="400px"))
    bar.add_xaxis(list(data["word"])[:-1][::-1])
    bar.add_yaxis("热度", list(data["hot"])[:-1][::-1])
    # 折线（区域）图、柱状（条形）图、K线图 : {a}（系列名称），{b}（类目值），{c}（数值）, {d}（无）
    # 散点图（气泡）图 : {a}（系列名称），{b}（数据名称），{c}（数值数组）, {d}（无）
    # 地图 : {a}（系列名称），{b}（区域名称），{c}（合并数值）, {d}（无）
    # 饼图、仪表盘、漏斗图: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    # 示例：formatter: '{b}: {@score}'
    bar.set_series_opts(label_opts=options.LabelOpts(is_show=True, formatter="{b}-{c}", font_size=12, color="yellow",
                                                     font_weight="bold"))
    bar.set_global_opts(title_opts=options.TitleOpts(title="微博热搜排行榜", pos_left="40%"),
                        # 坐标轴配置项
                        yaxis_opts=options.AxisOpts(is_show=True,
                                                    # y轴标签配置项
                                                    axislabel_opts=options.LabelOpts(is_show=False),
                                                    # 不显示网格线
                                                    splitline_opts={"show": False},
                                                    # 不显示y轴刻度线
                                                    axistick_opts={"show": False}
                                                    ),
                        xaxis_opts=options.AxisOpts(splitline_opts={"show": False}),
                        # 图例配置项
                        legend_opts=options.LegendOpts(is_show=False),
                        # 提示框配置项
                        tooltip_opts=options.TooltipOpts(is_show=True,
                                                         axis_pointer_type="line"  # 指示器样式
                                                         ),
                        # 区域缩放
                        datazoom_opts=options.DataZoomOpts(is_show=True,
                                                           type_="inside",          # 组件类型
                                                           orient="vertical"        # 垂直
                                                           ),
                        # 视觉映射
                        visualmap_opts=options.VisualMapOpts(is_show=True, type_="color",
                                                             range_color="",
                                                             pos_top="middle", pos_left="2%",
                                                             range_text=["High", "Low"]
                                                             )
                        )

    bar.reversal_axis()

    return bar


@app.route("/hotSearchData")
def get_hotSearch_bar():
    # data = pd.read_csv("spider/weibo/files/hotSearch.csv", encoding="utf-8")
    result = db.session.execute(
        text("select * from hotSearch where timeStamp in (select max(timeStamp) from hotSearch)")).fetchall()
    # data = [{"word": row[1], "hot": row[2], "href": row[3], "timeStamp": row[4]} for row in result]
    word = []
    hot = []
    href = []
    timeStamp = []
    for i in result:
        word.append(i[1])
        hot.append(i[2])
        href.append(i[3])
        timeStamp.append(i[4])
    data = {"word": word, "hot": hot, "href": href, "timeStamp": timeStamp}
    # print(data)

    c = hotSearch_bar(data)
    return c.dump_options_with_quotes()


@app.route("/topicData")
def topicData():
    result = db.session.execute(text(
        "select * from topic where timeStamp in (select max(timeStamp) from topic)"
    )).fetchall()
    word = []
    summary = []
    read = []
    mention = []
    href = []
    link = []
    for i in result:
        word.append(i[1])
        summary.append(i[2])
        read.append(i[3])
        mention.append(i[4])
        href.append(i[5])
        link.append(i[7])
    data = {"word": word, "summary": summary, "read": read, "mention": mention, "href": href, "link": link}

    return data


# 实现页面跳转

@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route("/hotSearchPage")
def hotSearchPage():
    return render_template("hotsearch.html")


@app.route("/topicPage", methods=["GET", "POST"])
def topicPage():
    return render_template("topic.html")


@app.route("/othersPage")
def othersPage():
    return render_template("others.html")


@app.route("/detailTopic", methods=["POST", "GET"])
def detailTopic():
    data = topicData()
    hrefs = [data["data"][i]["链接"] for i in data["data"]]
    print(hrefs)

    return render_template("detailTopic.html")


if __name__ == '__main__':
    app.run(debug=True)
