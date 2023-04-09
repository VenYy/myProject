from flask import Flask, render_template, url_for, redirect, jsonify
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts import options
from pyecharts.globals import ThemeType
import pandas as pd
import json

app = Flask(__name__)


def hotSearch_bar(data):
    bar = Bar(init_opts=options.InitOpts(theme=ThemeType.MACARONS, width="800px", height="400px"))
    bar.add_xaxis(list(data["词条"])[:10][::-1])
    bar.add_yaxis("热度", list(data["热度"])[:10][::-1])
    # 折线（区域）图、柱状（条形）图、K线图 : {a}（系列名称），{b}（类目值），{c}（数值）, {d}（无）
    # 散点图（气泡）图 : {a}（系列名称），{b}（数据名称），{c}（数值数组）, {d}（无）
    # 地图 : {a}（系列名称），{b}（区域名称），{c}（合并数值）, {d}（无）
    # 饼图、仪表盘、漏斗图: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    # 示例：formatter: '{b}: {@score}'
    bar.set_series_opts(label_opts=options.LabelOpts(is_show=True, formatter="{b}-{c}", font_size=10, color="white"))
    bar.set_global_opts(title_opts=options.TitleOpts(title="微博热搜榜单", pos_left="5%"),
                        # y轴配置项
                        yaxis_opts=options.AxisOpts(is_show=True,
                                                    # y轴标签配置项
                                                    axislabel_opts=options.LabelOpts(is_show=False)))
    bar.reversal_axis()

    return bar


@app.route("/hotSearchData")
def get_hotSearch_bar():
    data = pd.read_csv("spider/weibo/files/hot_band_bak.csv", encoding="utf-8")
    c = hotSearch_bar(data)
    return c.dump_options_with_quotes()


@app.route("/topicData")
def topicData():
    with open("spider/weibo/files/topic_band.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data
# 实现页面跳转

@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")

@app.route("/hotSearchPage")
def hotSearchPage():
    return render_template("hotsearch.html")


@app.route("/topicPage")
def topicPage():
    return render_template("topic.html")


@app.route("/othersPage")
def othersPage():
    return render_template("others.html")


if __name__ == '__main__':
    app.run(debug=True)