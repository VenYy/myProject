function topic() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/topicData",
        dataType: "json",
        success: function (data) {
            // $("#word").html(data["data"][0]["话题名称"])
            // $("#summary").html(data["data"][0]["导语"])
            // $("#talk").html("讨论量："+ data["data"][0]["讨论量"])
            // $("#read").html("阅读量："+ data["data"][0]["阅读量"])
            var str = ""
            for (let i = 0; i < data["data"].length; i++) {
                str += "<div class='topic' id='topic'>" + "<a href='" + data['data'][i]['链接']  + "'>"
                str += "<p id='word'>" + data['data'][i]['话题名称'] + "</p>"
                str += "<p id='summary'>" + data['data'][i]['导语'] + "</p>"
                str += "<p id='talk'>讨论量：" + data['data'][i]['讨论量'] + "</p>"
                str += "<p id='read'>阅读量：" + data['data'][i]['阅读量'] + "</p>"
                str += "</a></div>"
            }
            console.log(str)
            $(".topics").append(str);

        }
    })
}

topic()