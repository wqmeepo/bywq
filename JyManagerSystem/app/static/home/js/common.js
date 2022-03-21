function sidebarClick() {
    var link_name = window.location.href.split('/').slice(-1)
    ("#" + link_name).addClass("active")
}