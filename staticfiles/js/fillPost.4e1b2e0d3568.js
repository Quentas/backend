//let url = "https://fierce-dusk-92502.herokuapp.com";
let url = "http://127.0.0.1:8000/";
function fillPostHTML(type, postJSON){
    console.log(postJSON)
    function getName(postJSON){
        if(postJSON['user']['first_name'] == "" && postJSON['user']['last_name'] == "")
            return postJSON['user']['username'];
        else if(postJSON['user']['first_name'] != "" && postJSON['user']['last_name'] == "")
            return postJSON['user']['last_name'];
        else 
            return postJSON['user']['first_name'];
    }
    function getTimeHTML(postJSON){
        function formatDate(date){
            function pad(s) { return (s < 10) ? '0' + s : s; }
            var d = new Date(date)
            return pad(d.getDate()) + "/" + pad(d.getMonth()+1) + "/" + d.getFullYear()+ " " + pad(d.getHours())+":"+ pad(d.getMinutes());
        }
        let date = formatDate(new Date(postJSON['date']).toString());
        let last_edited = formatDate(new Date(postJSON['last_edited']).toString())
        return (date == last_edited) ? date : date+' (last edited: '+ last_edited +')';
    }
    function fillImages(postJSON){
        let images = postJSON['images'];
        let result = "";
        for(let i = 0; i < images.length; i++)
            result += '<div class="postImage" onclick="openImage(event, this)" style="background-image:url(https://fierce-dusk-92502.herokuapp.com'+images[i]['image']+');"></div>';
        return '<div class="postImages" id="postImages_' + postJSON['id']+'" >' + result + '</div>';
    }
    switch(type){
        case "post":
            return '<div class="post" id="post_' + postJSON['id'] + '" onclick="showPost(event, ' + postJSON['id'] + ')">' +
                        '<div class="postInner">' +
                            '<div class="authorAvatarBlock">' +
                                '<div onclick="showUser('+postJSON['user']['username']+')">' +
                                    '<img class="authorAvatar" src="https://fierce-dusk-92502.herokuapp.com' + postJSON['user']['profile_photo'] + '">' +
                                '</div>' +
                            '</div>' +
                            '<div class="postBlock">' +
                                '<div>' + 
                                    '<span class="Username" onclick="showUser('+postJSON['user']['username']+')">' + getName(postJSON) + '</span><span class="tag">@' + postJSON['user']['username'] + ' · ' + getTimeHTML(postJSON) + '</span>' +
                                '</div>' +
                                '<div class="postContent" id="postContent_'+postJSON['id']+'">' + (postJSON['content']+"") + '</div>' +                               
                                    fillImages(postJSON) +                               
                                '<div class="other">' +
                                    '<button id="commentsBtn_'+postJSON['id']+'" class="comment_btn" onclick="createComment(' + postJSON['id'] + ', 1)">' + postJSON['comments_count'] + '</button>' +
                                    '<button id="repostBtn_'+postJSON['id']+'" class="repost_btn" onclick="repostPost(' + postJSON['id'] + ', 1)">0</button>' +
                                    '<button id="likeBtn_'+postJSON['id']+'" class="like_btn" onclick="likePost(' + postJSON['id'] + ', 1)">0</button>' +
                                    '<button id="addToBookmarkBtn_'+postJSON['id']+'" class="addToBookmark_btn" onclick="addToBookmark(' + postJSON['id'] + ', 1)"></button>' +
                                '</div>' +
                            '</div>' +
                            '<div id="postSettings">...</div>';
        case "comment": 
            return '<div class="post" id="comment_' + postJSON['id'] + '" onclick="showComment(event, ' + postJSON['id'] + ')">' +
                        '<div class="postInner">' +
                            '<div class="authorAvatarBlock">' +
                                '<a href="user/' + postJSON['user']['username'] + '">' +
                                    '<img class="authorAvatar" src="https://fierce-dusk-92502.herokuapp.com' + postJSON['user']['profile_photo'] + '">' +
                                '</a>' +
                            '</div>' +
                            '<div class="postBlock">' +
                                '<div>' +
                                    '<a class="Username" href="#">' + getName(postJSON) + '</a><span class="tag">@' + postJSON['user']['username'] + ' · ' + getTimeHTML(postJSON) + '</span>' +
                                '</div>' +
                                '<div class="postContent" id="postContent__isComment_'+postJSON['id']+'">' + (postJSON['content']+"") + '</div>' +
                                '<div class="other">' +
                                    '<button id="commentsBtn__isComment_'+postJSON['id']+'" class="comment_btn" onclick="createComment(' + postJSON['id'] + ', 0)">' + postJSON['comments_count'] + '</button>' +
                                    '<button id="repostBtn__isComment_'+postJSON['id']+'" class="repost_btn" onclick="repostPost(' + postJSON['id'] + ', 0)">0</button>' +
                                    '<button id="likeBtn__isComment_'+postJSON['id']+'" class="like_btn" onclick="likePost(' + postJSON['id'] + ', 0)">0</button>' +
                                    '<button id="addToBookmarkBtn__isComment_'+postJSON['id']+'" class="addToBookmark_btn" onclick="addToBookmark(' + postJSON['id'] + ', 0)"></button>' +
                                '</div>' +
                            '</div>' +
                            '<div id="postSettings">...</div>';
        default: break;
    }
}

let Overlay = document.getElementById("Overlay");
Overlay.style.height = screen.height + "px";
let EngageHolder = document.getElementById("EngageHolder");
let Login = document.getElementById("Login");
let Registration = document.getElementById("Registration");
let openedPost = document.getElementById("openedPost");
let Forgot = document.getElementById("Forgot");
let startLocation = (document.location + "").split('#')[0];
let lastOpenedPost = "";
let lastOpenedUser = "";
let inputSearch = document.getElementById("searchInput");
let openedImage = document.getElementById('openedImage');
let Exit = document.getElementById('Exit');
let PopUp = document.getElementById('PopUp');
let body = document.getElementsByTagName('body')[0];
let Profile = document.getElementById('ProfilePage');
let feed_subscriptions = document.getElementById('feed_subscriptions');
let addImageInput = document.getElementById('addImageInput');
let newPostImages = document.getElementById('newPostImages');
let pageWrapper__Overlay = document.getElementById("pageWrapper__Overlay");