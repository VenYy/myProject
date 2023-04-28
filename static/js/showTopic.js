var current_page = 1
function topic() {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/topicData",
        data: {
            "page": current_page
        },
        dataType: "json",
        success: function (data) {
            console.log(data)
            data = data.data
            loading = false
            var str = ""
            if (data["href"].length > 0) {
                for (let i = 0; i < data["word"].length; i++) {
                    var word = data["word"][i]
                    var href = data['href'][i]
                    // str += "<div class='topic' id='topic'>" + "<a href='" + data['data'][i]['链接'] + "'>"
                    var publicTime = new Date(data["timeStamp"][i])
                    // 分页div
                    str += `<div class="topic-wrapper">`
                    str += `<div class='topic' onclick='openwindow("${word}")' data-read=${data['read'][i]} data-mention=${data['mention'][i]} data-publictime="${publicTime}">`
                    str += `<p id='word'>${data['word'][i]}</p>`
                    str += `<p id='summary'>${data['summary'][i]}</p>`
                    if (data['mention'][i] > 3000) {
                        str += `<p id="mention">讨论量：` + data["mention"][i] + `<span class='hot'><img src='static/images/hot.svg' alt='' ></span>` + "</p>"
                    } else {
                        str += `<p id='mention'>讨论量：${data['mention'][i]} </p>`
                    }
                    str += `<p id='read'>阅读量：` + data['read'][i] + "</p>"
                    str += `<a class='transPage' id='analyse' data-href="${href}" href="/topic/${word}" target="_blank">话题分析</a>`
                    str += `<a class='transPage' id='from' href=${data['link'][i]} >微博页面</a>`
                    // str += "</a></div>"
                    str += "</div>"
                    str += "</div>"
                }
                // console.log(str)
                $(".topics").append(str);
                current_page ++
                // 数据成功加载，重新绑定滚动事件监听器
                $(window).on("scroll", scrollHandler);
            }
            else {
                // 数据已全部加载完毕，滚动页面加载数据不再执行
                $(window).off("scroll", topic);
            }

        }
    })
}

var loading = false;        // 用于标志是否需要加载数据
var scrollHandler = function() {
    var scrollTop = $(this).scrollTop();        // 获取当前页面滚动位置
    var scrollHeight = $(document).height();    // 获取整个文档的高度
    var windowHeight = $(this).height();        // 获取当前窗口的高度
    console.log("页面滚动位置：" + scrollTop + ", 整个文档的高度：" + scrollHeight + ", 当前窗口的高度：" + windowHeight)
    if (!loading && scrollTop + windowHeight >= scrollHeight - 100) {
        loading = true;
        console.log("滚动事件被触发")
        topic();
    }
    console.log(loading)
};

$(document).ready(function() {
    // 获取初始数据
    topic();
    // 绑定滚动事件监听器
    $(window).on("scroll", scrollHandler);
});



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
    } else {
        topics.sort(function (a, b) {
            return $(a).data("read") - $(b).data("read")
        })
    }
    $(".topics").empty().append(topics)
    ascRead = !ascRead
}

// 按照发布时间排序
var ascTime = true

function sortTime() {
    var topics = $.makeArray($(".topics .topic"))
    if (ascTime) {
        topics.sort(function (a, b) {
            // js大小写不敏感。。。。。驼峰命名无效
            console.log(new Date($(b).data("publictime")) - new Date($(a).data("publictime")))
            return new Date($(b).data("publictime")) - new Date($(a).data("publictime"))
        })
    } else {
        topics.sort(function (a, b) {
            return new Date($(a).data("publictime")) - new Date($(b).data("publictime"))
        })
    }
    $(".topics").empty().append(topics)
    ascTime = !ascTime
}


function openwindow(topic_name) {
    var modal = document.getElementById("modal")
    var topics = document.querySelectorAll(".topic")
    console.log(topics)
    // 判断被点击的元素是否为链接，若不是，则弹出窗口
    for (var i = 0; i < topics.length; i++) {
        var topic = topics[i]
        topic.addEventListener("click", function (event) {
            if (!event.target.closest("a")) {
                modal.style.display = "inline-block"
            }
        })
    }
    // 按下Escape键后关闭窗口
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            document.getElementById("modal").style.display = "none"
        }
    })

    document.getElementById("container").innerText = "This topic name is: " + topic_name

}


function closewindow() {
    document.getElementById("modal").style.display = "none"
}

