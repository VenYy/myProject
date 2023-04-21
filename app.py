import csv
import json
import os

from flask import Flask, render_template, url_for, redirect, jsonify, request
from pyecharts.charts import Bar, Timeline, Grid, Line, Pie
from pyecharts import options
from pyecharts.globals import ThemeType
from spider.weibo.DBManager import *
from spider.weibo.searchTrend import *

# from flask_cors import CORS

app = Flask(__name__)
# 启用CORS允许跨域请求
# CORS(app)

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
os.chdir("/media/venyy/Codes/project/")


# 绘制Top热搜柱状图
def hotSearch_bar(data):
    bar = Bar(init_opts=options.InitOpts(theme=ThemeType.MACARONS, width="1600px", height="600px"))
    bar.add_xaxis(list(data["word"])[:-1][::-1])
    bar.add_yaxis("热度", list(data["hot"])[:-1][::-1])
    # 折线（区域）图、柱状（条形）图、K线图 : {a}（系列名称），{b}（类目值），{c}（数值）, {d}（无）
    # 散点图（气泡）图 : {a}（系列名称），{b}（数据名称），{c}（数值数组）, {d}（无）
    # 地图 : {a}（系列名称），{b}（区域名称），{c}（合并数值）, {d}（无）
    # 饼图、仪表盘、漏斗图: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    # 示例：formatter: '{b}: {@score}'
    bar.set_series_opts(label_opts=options.LabelOpts(is_show=True,
                                                     formatter="{b}-{c}",
                                                     font_size=12,
                                                     color="yellow",
                                                     font_weight="bold"))
    bar.set_global_opts(title_opts=options.TitleOpts(title="微博热搜排行榜", pos_left="40%",
                                                     subtitle="更新时间：" + str(data["timeStamp"][0]),
                                                     subtitle_textstyle_opts={"color": "darkgreen"}
                                                     ),
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
                                                           type_="inside",  # 组件类型
                                                           orient="vertical"  # 垂直
                                                           ),
                        # 视觉映射
                        visualmap_opts=options.VisualMapOpts(is_show=True, type_="color",
                                                             range_color="",
                                                             pos_top="10%", pos_left="5%",
                                                             orient="vertical",
                                                             range_text=["High", "Low"]
                                                             ),
                        graphic_opts=options.GraphicGroup(graphic_item=options.GraphicItem(top="50px"))
                        )

    bar.reversal_axis()

    return bar


# 绘制热搜趋势折线图
# 热搜趋势-阅读量
def searchTrendRead_line(data):
    line = Line(init_opts=options.InitOpts(width="1000px", height="400px"))
    line.set_global_opts(title_opts=options.TitleOpts(title="热搜趋势-阅读量", pos_left="40%"),
                         legend_opts=options.LegendOpts(is_show=True,
                                                        pos_left="15%", pos_top="10%",
                                                        orient="vertical",
                                                        textstyle_opts=options.TextStyleOpts(color="#101712"),
                                                        border_width=1,
                                                        border_color="green",
                                                        border_radius=5),
                         tooltip_opts=options.TooltipOpts(is_show=True, trigger="axis"),
                         datazoom_opts=options.DataZoomOpts(is_show=True, type_="inside"))
    line.add_xaxis(list(data["time"]))
    line.add_yaxis(data["word"][0], list(data["read"][0]))
    line.add_yaxis(data["word"][1], list(data["read"][1]))
    line.add_yaxis(data["word"][2], list(data["read"][2]))
    line.add_yaxis(data["word"][3], list(data["read"][3]))
    line.add_yaxis(data["word"][4], list(data["read"][4]))

    # 折线粗细
    line.set_series_opts(linestyle_opts=options.LineStyleOpts(width=3))

    return line


# 热搜趋势-讨论量
def searchTrendMention_line(data):
    line = Line(init_opts=options.InitOpts(width="1000px", height="400px"))
    line.set_global_opts(title_opts=options.TitleOpts(title="热搜趋势-讨论量", pos_left="40%"),
                         legend_opts=options.LegendOpts(is_show=True,
                                                        pos_left="15%", pos_top="10%",
                                                        orient="vertical",
                                                        textstyle_opts=options.TextStyleOpts(color="#101712"),
                                                        border_width=1,
                                                        border_color="green",
                                                        border_radius=5),
                         tooltip_opts=options.TooltipOpts(is_show=True, trigger="axis"),
                         datazoom_opts=options.DataZoomOpts(is_show=True, type_="inside"))
    line.add_xaxis(list(data["time"]))
    line.add_yaxis(data["word"][0], list(data["mention"][0]))
    line.add_yaxis(data["word"][1], list(data["mention"][1]))
    line.add_yaxis(data["word"][2], list(data["mention"][2]))
    line.add_yaxis(data["word"][3], list(data["mention"][3]))
    line.add_yaxis(data["word"][4], list(data["mention"][4]))

    # 折线粗细
    line.set_series_opts(linestyle_opts=options.LineStyleOpts(width=3))

    return line


# 热搜趋势-原创人数
def searchTrendOri_line(data):
    line = Line(init_opts=options.InitOpts(width="1000px", height="400px"))
    line.set_global_opts(title_opts=options.TitleOpts(title="热搜趋势-原创人数", pos_left="40%"),
                         legend_opts=options.LegendOpts(is_show=True,
                                                        pos_left="15%", pos_top="10%",
                                                        orient="vertical",
                                                        textstyle_opts=options.TextStyleOpts(color="#101712"),
                                                        border_width=1,
                                                        border_color="green",
                                                        border_radius=5),
                         tooltip_opts=options.TooltipOpts(is_show=True, trigger="axis"),
                         datazoom_opts=options.DataZoomOpts(is_show=True, type_="inside"))
    line.add_xaxis(list(data["time"]))
    line.add_yaxis(data["word"][0], list(data["ori"][0]))
    line.add_yaxis(data["word"][1], list(data["ori"][1]))
    line.add_yaxis(data["word"][2], list(data["ori"][2]))
    line.add_yaxis(data["word"][3], list(data["ori"][3]))
    line.add_yaxis(data["word"][4], list(data["ori"][4]))

    # 折线粗细
    line.set_series_opts(linestyle_opts=options.LineStyleOpts(width=3))

    return line


@app.route("/api/searchTrendData")
def searchTrend():
    with open("spider/weibo/files/trend.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # print(data["data"])
    word = []
    read = []
    mention = []
    ori = []
    time = []
    for i in data["data"]:
        # print(i["word"])
        word.append(i["word"])
        r = []
        m = []
        o = []
        # time.append(i["read"][j]["time"] for j in range(len(i["read"])))
        for j in range(len(i["read"])):
            # print(i["read"][j]["time"])
            t = i["read"][j]["time"]
            r.append(i["read"][j]["value"])
            m.append(i["mention"][j]["value"])
            o.append(i["ori"][j]["value"])
            if t not in time:
                time.append(t)

        read.append(r)
        mention.append(m)
        ori.append(o)
    data = {"word": word, "read": read, "mention": mention, "ori": ori, "time": time}
    print(data)
    readLine = searchTrendRead_line(data)
    mentionLine = searchTrendMention_line(data)
    oriLine = searchTrendOri_line(data)
    return [readLine.dump_options_with_quotes(),
            mentionLine.dump_options_with_quotes(),
            oriLine.dump_options_with_quotes()]


@app.route("/api/hotSearchData")
def get_hotSearch_bar():
    # data = pd.read_csv("spider/weibo/files/hotSearch.csv", encoding="utf-8")
    result = db.session.execute(
        text("select * from hotSearch where timeStamp in (select max(timeStamp) from hotSearch)")).fetchall()
    db.session.commit()
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
    print(data)

    c = hotSearch_bar(data)
    return c.dump_options_with_quotes()


@app.route("/api/topicData")
def topicData():
    result = db.session.execute(text(
        "select * from topic where timeStamp in (select max(timeStamp) from topic)"
    )).fetchall()
    db.session.commit()
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


@app.route("/hotSearchPage", methods=["GET", "POST"])
def hotSearchPage():
    d = db.session.execute(
        text(f"select * from searchTrend order by timestamp desc limit 10")
    )
    db.session.commit()
    if request.method == "POST":
        key = request.form["search"]
        if len(key) == 0:
            pass
        else:
            data = db.session.execute(
                text(f"select * from searchTrend where word like '%{key}%'")
            ).fetchall()
            db.session.commit()
            return render_template("hotsearch.html", data=data)
    return render_template("hotsearch.html", data=d)


@app.route("/topicPage", methods=["GET", "POST"])
def topicPage():
    return render_template("topic.html")


@app.route("/othersPage")
def othersPage():
    return render_template("others.html")


@app.route("/topic/api/<word>", methods=["POST", "GET"])
def detailTopicApi(word):
    data = db.session.execute(
        text(f"select * from topicDetail where topic_name = '{word}'")
    ).fetchall()
    db.session.commit()
    result = []

    for i in data:
        result.append({"mid": i[0],
                       "detail_url": i[1],
                       "screen_name": i[2],
                       "gender": i[4],
                       "profile_url": i[5],
                       "followers_count": i[6],
                       "status_province": i[7],
                       "topic_name": i[9],
                       "attitudes_count": i[10],
                       "comments_count": i[11],
                       "reposts_count": i[12],
                       "text": i[13],
                       "timeStamp": i[14]})

    gender = [i[4] for i in data]
    province = [i[7] for i in data]

    gender_counts = [(g, gender.count(g)) for g in set(gender)]
    province_counts = sorted([(p, province.count(p)) for p in set(province)], key=lambda x: x[1])[::-1]
    if len(province_counts) > 5:
        province_counts = province_counts[:5]
    else:
        pass
    print(province_counts)

    pie = (Pie(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
           .add("", gender_counts,
                rosetype="radius",  # 南丁格尔玫瑰图
                center=["20%", "50%"],
                radius="60%")
           .add("", province_counts,
                rosetype="radius",
                center=["70%", "50%"],
                radius="60%", )
           .set_global_opts(title_opts=options.TitleOpts(title=word, pos_left="5%",
                                                         title_link="",
                                                         title_textstyle_opts=options.TextStyleOpts(font_size=20,
                                                                                                    font_weight="bold")),
                            legend_opts=options.LegendOpts(pos_right="10%"))
           .set_series_opts()
           )
    return [result, pie.dump_options_with_quotes()]


@app.route("/topic/<word>", methods=["GET", "POST"])
def detailTopic(word):
    return render_template("detailTopic.html", word=word)


if __name__ == '__main__':
    app.run(debug=True)
