window.setTimeout(function () {
    window.document.getElementById("windowLoading").style.display = "none";
    window.document.getElementById("main").style.display = "";
}, 1000)


$.ajax({
    type: "GET",
    url: "/topic/<word>",
    success: function (data) {
        console.log(data)
    }
})