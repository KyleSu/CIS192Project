
function searchUser() {
    event.preventDefault();
    console.log($('#username').val());
    var username = $('#username').val();
    if (username === "") {
        alert("Empty username");
    } else {
        var postUsername = {
            name: username
        };

        console.log("hello: " + postUsername.name);

        $.post("/searchuser", postUsername, function (data) {
            if (data === "false") {
                alert("Username not found");
            } else {
                $("html").empty();
                $("html").append(data);
            }
        });
    }
}
function searchHashtag() {
    event.preventDefault();
    console.log($('#hashtag').val());
    var hashtag = $('#hashtag').val();
    if (hashtag === "") {
        alert("Empty hashtag");
    } else {
        var postHashtag = {
            hashtag: hashtag
        };

        console.log("hello: " + postHashtag.hashtag);

        $.post("/searchhashtag", postHashtag, function (data) {
            if (data === "false") {
                alert("Hashtag not found");
            } else {
                $("html").empty();
                $("html").append(data);
            }
        });
    }
}