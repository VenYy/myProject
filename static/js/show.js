function hot_search() {
    var chart = echarts.init(document.getElementById("hot_search"), {renderer: "canvas"});


    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/hotSearchData",
        dataType: "json",
        success: function (data) {
            console.log(data)
            chart.setOption(data)
        }
    });


}

hot_search()
setInterval(hot_search, 1000*60)