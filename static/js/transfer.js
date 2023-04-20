// // 导航栏实现页面跳转
// function turnTopic() {
//     top.location.href = "http://127.0.0.1:5000/topicPage"
// }
//
// function turnHotSearch() {
//     top.location.href = "http://127.0.0.1:5000/hotSearchPage"
// }
//
// function turnHome() {
//     top.location.href = "http://127.0.0.1:5000/"
// }
//
// function turnOthers() {
//     top.location.href = "http://127.0.0.1:5000/othersPage"
// }



function turnBg() {
    var currentUrl = window.location.href;
    // console.log(currentUrl)
    var links = document.getElementsByClassName("index_a");
    // console.log(links)
    for (var i = 0; i < links.length; i ++) {
        var link = links[i];
        // console.log(link.baseURI)
        if (link.getAttribute("href") === currentUrl) {
            link.style.color = "#373638"
            link.style.backgroundColor = "#ebeced"
        }
    }
}

turnBg()