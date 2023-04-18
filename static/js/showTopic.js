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
            for (let i = 0; i < data["word"].length; i++) {
                // str += "<div class='topic' id='topic'>" + "<a href='" + data['data'][i]['链接'] + "'>"
                str += `<div class='topic' id='topic' data-read=${data['read'][i]} data-mention=${data['mention'][i]}>`
                str += `<p id='word'>${data['word'][i]}</p>`
                str += `<p id='summary'>${data['summary'][i]}</p>`
                if (data['mention'][i] > 2000) {
                    str += `<p id="mention">讨论量：` + data["mention"][i] + `<span class='hot'><img src='static/images/hot.svg' alt='' ></span>` + "</p>"
                } else {
                    str += `<p id='mention'>讨论量：${data['mention'][i]} </p>`
                }
                str += `<p id='read'>阅读量：` + data['read'][i] + "</p>"
                var word = data['word'][i]
                var href = data['href'][i]
                str += `<a class='transPage' id='analyse' data-href="${href}" href="/topic/${word}" target="_blank">话题分析</a>`
                str += `<a class='transPage' id='from' href=${data['link'][i]} >微博页面</a>`
                // str += "</a></div>"
                str += "</div>"
            }
            // console.log(str)
            $(".topics").append(str);

        }
    })
}


// 话题搜索功能
function search() {
    var input = document.getElementById("searchBox").value.toLowerCase();
    var divs = document.getElementsByClassName("topics")[0].getElementsByTagName("div");
    for (var i = 0; i < divs.length; i++) {
        var text = divs[i].textContent.toLowerCase();
        if (text.includes(input)) {
            divs[i].classList.remove("hide");
        } else {
            divs[i].classList.add("hide");
        }
    }
}

// 回车执行搜索
document.getElementById("searchBox").addEventListener("keyup", function (event) {
    // 判断是否按下回车键
    if (event.keyCode === 13) {
        // 调用search()函数
        search();
    }
});


// 按照讨论量排序
var ascMention = true

function sortMention() {
    var topics = $.makeArray($(".topics .topic"))
    if (ascMention) {        // 升序
        topics.sort(function (a, b) {
            return $(b).data("mention") - $(a).data("mention")
        })
    } else {                 // 降序
        topics.sort(function (a, b) {
            return $(a).data("mention") - $(b).data("mention")
        })
    }
    $(".topics").empty().append(topics)
    ascMention = !ascMention

}

// 按照阅读量排序
var ascRead = true
function sortRead() {
    var topics = $.makeArray($(".topics .topic"))
    if (ascRead) {
        topics.sort(function (a, b) {
            return $(b).data("read") - $(a).data("read")
        })
    }
    else {
        topics.sort(function (a, b) {
            return $(a).data("read") - $(b).data("read")
        })
    }
    $(".topics").empty().append(topics)
    ascRead = !ascRead
}


// 当页面滚动到某个位置时，再加载需要延迟加载的内容
window.addEventListener('scroll', function () {
    if (window.pageYOffset > 1000) { // 页面向下滚动超过 1000 像素时
        var lazyLoadDiv = document.getElementsByClassName("topic");
        if (!lazyLoadDiv.innerHTML) { // 避免重复加载
            lazyLoadDiv.innerHTML = 'waiting';
        }
    }
});

topic()