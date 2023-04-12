import pandas as pd

from pyecharts.charts import Bar, Timeline, Grid
from pyecharts import options


data = pd.read_csv("./files/hotSearch.csv", encoding="utf-8")
# a = list(data["词条"])
# print(a[1:10])


def show():
    bar = Bar()
    tl = Timeline()
    grid = Grid()
    print(list(data["word"])[:10])
    bar.set_global_opts(title_opts=options.TitleOpts(title="微博热搜榜单"))
    bar.add_yaxis("热度", list(data["hot"])[:10])
    bar.add_xaxis(list(data["word"])[:10])
    bar.reversal_axis()
    bar.set_series_opts(label_opts=options.LabelOpts(position="right"))
    tl.add(bar, "a")

    grid.add(bar, grid_opts=options.GridOpts(pos_left="25%", pos_right="0%"))
    tl.add(grid, "")

    tl.render()


def showList():
    tl = Timeline()
    for i in range(60):         # 60分钟
        bar = Bar(init_opts=options.InitOpts(width="900px", height="900px"))
        grid = Grid()
        # print(list(data["时间"])[i*50])
        # print(list(data["词条"])[i * 50:i * 50 + 50])
        # print(list(data["热度"])[i * 50:i * 50 + 50])
        bar.set_global_opts(title_opts=options.TitleOpts())
        bar.add_yaxis("热度", list(data["hot"])[i * 50:i * 50 + 15][::-1])
        bar.add_xaxis(list(data["word"])[i * 50:i * 50 + 15][::-1])
        bar.reversal_axis()
        bar.set_series_opts(label_opts=options.LabelOpts(position="right"))
        tl.add(bar, list(data["timeStamp"])[i*50].split("  ")[1])

        grid.add(bar, grid_opts=options.GridOpts(pos_left="25%", pos_right="0%"))
        tl.add(grid, "{}".format(list(data["timeStamp"])[i*50]))
        tl.add_schema(play_interval=200,        # 播放速度
                      is_timeline_show=True,   # 是否显示timeline组件
                      is_auto_play=False        # 是否自动播放
                      )

    tl.render()


show()