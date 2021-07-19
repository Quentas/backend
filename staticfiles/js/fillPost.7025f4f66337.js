
async function executeRequest(url, method, body = null, headers = null){
    headers = (headers == null) ? {'Content-Type' : 'application/json'} : headers;
    body = (body == null) ? null : JSON.stringify(body);
    return await fetch("https://fierce-dusk-92502.herokuapp.com/" + url,{
    //return await fetch("http://127.0.0.1:8000/" + url,{
        method : method,
        body : body,
        headers : headers
    }).then(response => {
        return response.json()
    })
    .catch(err => console.log(err))
}

function fillPostHTML(type, postJSON){
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
        if(images.length != 0){
            for(let i = 0; i < images.length; i++){
                result += '<img class="postImage" src="'+images[i]['image']+'"></img>';
            }
            return '<div class="postImages" id="postImages_' + postJSON['id']+'" >' + result + '</div>';
        }
        return;
    }
    switch(type){
        case "post":
            return '<div class="post" id="post_' + postJSON['id'] + '">' +
                        '<div class="postInner">' +
                            '<div class="authorAvatarBlock">' +
                                '<a href="user/' + postJSON['user']['username'] + '">' +
                                    '<img class="authorAvatar" src="https://fierce-dusk-92502.herokuapp.com' + postJSON['user']['profile_photo'] + '">' +
                                '</a>' +
                            '</div>' +
                            '<div class="postBlock">' +
                                '<div>' +
                                    '<a class="authorUsername" href="#">' + getName(postJSON) + '</a><span class="postInfo">@' + postJSON['user']['username'] + ' · ' + getTimeHTML(postJSON) + '</span>' +
                                '</div>' +
                                '<div class="postContent" id="postContent_'+postJSON['id']+'" onclick="showPost(' + postJSON['id'] + ')">' + (postJSON['content']+"") + '</div>' +                               
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
            return '<div class="post" id="comment_' + postJSON['id'] + '">' +
                        '<div class="postInner">' +
                            '<div class="authorAvatarBlock">' +
                                '<a href="user/' + postJSON['user']['username'] + '">' +
                                    '<img class="authorAvatar" src="https://fierce-dusk-92502.herokuapp.com' + postJSON['user']['profile_photo'] + '">' +
                                '</a>' +
                            '</div>' +
                            '<div class="postBlock">' +
                                '<div>' +
                                    '<a class="authorUsername" href="#">' + getName(postJSON) + '</a><span class="postInfo">@' + postJSON['user']['username'] + ' · ' + getTimeHTML(postJSON) + '</span>' +
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