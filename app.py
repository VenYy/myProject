from flask import Flask, render_template, url_for, redirect
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts import options
import pandas as pd
app = Flask(__name__)


def hotSearch_bar(data):
    bar = Bar()
    grid = Grid()
    grid.add(bar, grid_opts=options.GridOpts(pos_left="50%", background_color="red"))
    bar.set_global_opts(title_opts=options.TitleOpts(title="微博热搜榜单"))
    bar.set_series_opts(label_opts=options.LabelOpts(is_show=False))
    bar.add_xaxis(list(data["词条"])[:10])
    bar.add_yaxis("热度", list(data["热度"])[:10])
    bar.reversal_axis()

    return bar

@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")

@app.route("/hotSearch")
def get_hotSearch_bar():
    data = pd.read_csv("spider/weibo/files/hot_band_bak.csv", encoding="utf-8")
    c = hotSearch_bar(data)
    return c.dump_options_with_quotes()


# @app.route("/show_hot_search")
# def show_hot_search():
#     return render_template("hot_search.html")


if __name__ == '__main__':
    app.run(debug=True)
