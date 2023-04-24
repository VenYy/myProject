window.setTimeout(function () {
    window.document.getElementById("windowLoading").style.display = "none";
    window.document.getElementById("wordCloud").style.display = "";
}, 2000)



var word = document.getElementById("word").value
$.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/topic/api/" + word,
    dataType: "JSON",
    success: function (result) {
        var data = result[0]
        let str = `
                <div class="row">
                <div class="cell">发布者</div>
                <div class="cell">性别</div>
                <div class="cell">粉丝数</div>
                <div class="cell">所在地区</div>
                <div class="cell">正文</div>
                <div class="cell">点赞数</div>
                <div class="cell">评论数</div>
                <div class="cell">转发数</div>
                <div class="cell">发布时间</div>
                </div>`
        for (let i = 0; i < data.length; i++) {
            let hiddenRow = ""
            if (((data[i]["attitudes_count"] < 3) && (data[i]["comments_count"] < 3)) || (data[i]["text"].length < 3)){
                hiddenRow = "hidden"
            }
            str += `<div class="row ${hiddenRow}">
                    <div class="cell"><a href="${data[i]['profile_url']}">${data[i]['screen_name']}</a></div>
                    <div class="cell">${data[i]['gender']}</div>
                    <div class="cell">${data[i]['followers_count']}</div>
                    <div class="cell">${data[i]['status_province']}</div>
                    <div class="cell" id="text"><a href="${data[i]['detail_url']}">${data[i]["text"]}</a></div>
                    <div class="cell">${data[i]['attitudes_count']}</div>
                    <div class="cell">${data[i]['comments_count']}</div>
                    <div class="cell">${data[i]["reposts_count"]}</div>
                    <div class="cell">${data[i]['timeStamp']}</div>
                </div>`
        }
        $(".divTable").append(str)

        var genderChart = echarts.init(document.getElementById("pie"), {renderer: "canvas"})
        genderChart.setOption(JSON.parse(result[1]))

        console.log(JSON.parse(result[2]))

        var wordCloudChart = echarts.init(document.getElementById("wordCloud"), {renderer: "canvas"})
        wordCloudChart.setOption(JSON.parse(result[2]))

    }
})


// 隐藏或显示可能无用的信息
window.onload = function () {
    var button = document.getElementById("hiddenBtn")
    button.onclick = function () {
        const elements = document.querySelectorAll('.hidden');
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = (elements[i].style.display === 'none') ? 'table-row' : 'none';
        }
    }

}