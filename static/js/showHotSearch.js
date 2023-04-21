function hot_search() {
    var chart = echarts.init(document.getElementById("hot_search"), {renderer: "canvas"});


    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/api/hotSearchData",
        dataType: "json",
        success: function (data) {
            // console.log(data)
            chart.setOption(data)
        }
    });
}

function trend_read() {
    var chart = echarts.init(document.getElementById("read"), {renderer: "canvas"})
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/api/searchTrendData",
        dataType: "json",
        success: function (data) {
            chart.setOption(JSON.parse(data[0]))
        }
    })
}

function trend_mention() {
    var chart = echarts.init(document.getElementById("mention"), {renderer: "canvas"})
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/api/searchTrendData",
        dataType: "json",
        success: function (data) {
            chart.setOption(JSON.parse(data[1]))
        }
    })
}


function trend_ori() {
    var chart = echarts.init(document.getElementById("ori"), {renderer: "canvas"})
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/api/searchTrendData",
        dataType: "json",
        success: function (data) {
            console.log(data)
            chart.setOption(JSON.parse(data[2]))
        }
    })
}


hot_search()
trend_read()
trend_mention()
trend_ori()

setInterval(hot_search, 1000*60)
setInterval(trend_read, 1000*60)
setInterval(trend_mention, 1000*60)
setInterval(trend_ori, 1000*60)