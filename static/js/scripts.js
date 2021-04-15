async function executeRequest(url, method, body = null, headers = null){
    headers = (headers == null) ? {'Content-Type' : 'application/json'} : headers;
    body = (body == null) ? null : JSON.stringify(body);
    //return await fetch("https://fierce-dusk-92502.herokuapp.com/" + url,{
    return await fetch("http://127.0.0.1:8000/" + url,{
        method : method,
        body : body,
        headers : headers
    }).then(response => {
        return response.json()
    })
    .catch(err => console.log(err))
}

let me = null;
executeRequest("auth/users/me", 'GET', null, {"Content-Type" : "application/json", "Authorization" : "Token "+window.localStorage.getItem("token")})
.then(myInfo => {
    try{
        if(myInfo['username'] != undefined){
            me = myInfo;
            document.getElementById('login').style.display = 'none';
            document.getElementById('registration').style.display = 'none';
            document.getElementById('logout').style.display = 'block';
            document.getElementById('myInfo').innerHTML = '<img id="userImg" src='+myInfo['profile_photo']+'>'+ myInfo['username']+'';
            loaderStarter();
        }
    }catch{
        document.getElementById('login').style.display = 'block';
        document.getElementById('registration').style.display = 'block';
        document.getElementById('logout').style.display = 'none';
        loaderStarter()
    }
});


function loaderStarter(){
        let s = 0, e = 5;
        function loader(){
            let usersCounter = 0, postsJSON = [], posts = [], usersJSON = [], users = [];
            executeRequest("api/v1/posts/?startpos="+s+"&endpos="+e, 'GET') // get ids from s to e
            .then(postsJSONs => {
                if(postsJSONs.length != 0){
                    document.getElementById('loadingAnimation_1').style.display = 'block';
                    postsJSONs.forEach(postJSON => {
                        postsJSON.push(postJSON);
                        users.push(postJSON['user']);
                        if(postsJSON.length == postsJSONs.length) // starts after all post have been loaded
                                [...new Set(users)].forEach(user => {
                                    executeRequest("auth/users/"+user, 'GET') //get user
                                    .then(userJSON => {
                                        usersJSON[user] = userJSON;
                                        usersCounter++;
                                        if(usersCounter == [...new Set(users)].length){ // starts after all users have been loaded
                                            postsJSONs.forEach(postJSON => {
                                                posts.push({"id" : postJSON['id'], "postHTML" : fillPostHTML("post", postJSON, usersJSON[postJSON['user']], me)});
                                                if(posts.length == postsJSONs.length){
                                                    posts.sort((a,b) => b.id - a.id);
                                                    let m = document.querySelector('main');
                                                    posts.forEach(post => {
                                                        m.innerHTML += post['postHTML'];
                                                    });
                                                    document.getElementById('loadingAnimation_1').style.display = 'none';
                                                }
                                            });
                                        }
                                    });
                                });
                    });
                }
                else{
                    return true;
                }
            });
            s = e;
            e += 5;
        }
        loader();
        let lastPageYOffset = 0;
        window.addEventListener('scroll', function k() {
            if(pageYOffset - lastPageYOffset >= 1250){
                if(loader()) window.removeEventListener('scroll', k);
                lastPageYOffset = pageYOffset;
            }
        });
}


function showComments(id, me){
    let usersCounter = 0, commentsJSON = [], comments = [], usersJSON = [], users = [];
    executeRequest("api/v1/comments/?post_id="+id, 'GET')
    .then(commentsJSONs => {
        document.getElementById('commentsBtn_'+id).onclick = "";
        document.getElementById('commentsBtn_'+id).addEventListener('click', () => {
            if(document.getElementById('commentsBlock_'+id).style.display == "block")
                document.getElementById('commentsBlock_'+id).style.display = "none";
            else
                document.getElementById('commentsBlock_'+id).style.display = "block";

        });
        document.getElementById('commentsBtn_'+id).click()
        if(commentsJSONs.length != 0){
            document.getElementById('loadingAnimation_1').style.display = 'block';
            commentsJSONs.forEach(commentJSON => {
                commentsJSON.push(commentJSON);
                users.push(commentJSON['user']);
                if(commentsJSON.length == commentsJSONs.length) // starts after all post have been loaded
                        [...new Set(users)].forEach(user => {
                            executeRequest("auth/users/"+user, 'GET') //get user
                            .then(userJSON => {
                                usersJSON[user] = userJSON;
                                usersCounter++;
                                if(usersCounter == [...new Set(users)].length){ // starts after all users have been loaded
                                    commentsJSONs.forEach(commentJSON => {
                                        comments.push({"id" : commentJSON['id'], "postHTML" : fillPostHTML("comment", commentJSON, usersJSON[commentJSON['user']], me)});
                                        if(comments.length == commentsJSONs.length){
                                            comments.sort((a,b) => b.id - a.id);
                                            let m = document.getElementById("commentsBlock_" + id);
                                            comments.forEach(post => {
                                                m.innerHTML += post['postHTML'];
                                            });
                                            document.getElementById('loadingAnimation_1').style.display = 'none';
                                        }
                                    });
                                }
                            });
                        });

            });
        }
    });
}

function fillPostHTML(type, postJSON, userJSON, me){
    function getTimeHTML(postJSON){
        function formatDate(date){
            function pad(s) { return (s < 10) ? '0' + s : s; }
            var d = new Date(date)
            return pad(d.getDate()) + "/" + pad(d.getMonth()+1) + "/" + d.getFullYear()+ " " + pad(d.getHours())+":"+ pad(d.getMinutes());
        }
        return (postJSON['date'] == postJSON['last_edited']) ? '<div id="datePosted_'+postJSON['id']+'" class="datePosted">'+formatDate(new Date(postJSON['date']).toString())+'</div>' : '<div id="datePosted_'+postJSON['id']+'" class="datePosted">'+formatDate(new Date(postJSON['date']).toString())+' (last edited: '+ formatDate(new Date(postJSON['last_edited']).toString()) +')</div>';
    }
    function getEditHTML(type, me, postJSON){
        if(me == undefined) return '';
        else
            switch(type){
                case "post": 
                    return (postJSON['user'] == me['id']) ? '<button class="edit_btn" onclick="editPostButton(1, '+postJSON['id']+')">Edit Post</button>' : ''
                case "comment":
                    return (postJSON['user'] == me['id']) ? '<button class="edit_btn" onclick="editPostButton(2, '+postJSON['id']+')">Edit Comment</button>' : '';
                default: break;
            }
    }
    switch(type){
        case "post":
            return '<div class="post" id="post_'+postJSON['id']+'">' +
                        '<div class="authorBlock">' +
                            '<img class="authorAvatar" src="'+userJSON['profile_photo']+'" alt="profile photo">' +
                            '<div class="authorBlock_inner">' +
                                '<div class="authorName">'+userJSON['username']+'</div>' +
                                getTimeHTML(postJSON) +
                            '</div>' +
                        '</div>' +
                        '<div class="contentBlock" id="post_content_'+postJSON['id']+'">'+postJSON['content']+'</div>' +
                        '<div class="other">' +
                            '<button id="commentsBtn_'+postJSON['id']+'" class="comment_btn" onclick="showComments('+postJSON['id']+')">Comments</button>' +
                            getEditHTML("post", me, postJSON) +
                        ' </div>' +
                        '<div class="commentsBlock" id="commentsBlock_'+postJSON['id']+'">'+
                            '<button class="addComment" onclick="createPostButton(1,'+postJSON['id']+')">Add Comment</button>'+
                        '</div>' +
                    '</div>';
        case "comment": 
            return '<div class="comment" id="comment_'+postJSON['id']+'">' +
                        '<div class="authorBlock">' +
                            '<img class="authorAvatar" src="'+userJSON['profile_photo']+'" alt="profile photo">'+
                            '<div class="authorBlock__inner">'+
                                '<div class="authorName">'+userJSON['username']+'</div>'+
                                getTimeHTML(postJSON) +
                            '</div>'+
                        '</div>'+
                        '<div class="contentBlock" id="comment_content_'+postJSON['id']+'">'+postJSON['content']+'</div>' +
                        '<div class="otherComment">'+
                            '<button class="otherCommentsButtons" onclick="createPostButton(2, '+postJSON['id']+')">Reply</button>'+
                            getEditHTML("comment", me, postJSON) +
                        '</div>'+
                    '</div>';
        default: break;
    }
}

function drawOverlay(){
    document.querySelector('body').innerHTML +=  '<div id="overlay" style="height:'+window.screen.availHeight + 'px; width:'+window.screen.availWidth + 'px"><button id="closeOverlay" onclick="removePW()">X</button><div id="overlay_inner"></div></div>';
}
//Edit
function editPostButton(type, id){
    drawOverlay();
    document.getElementById('overlay_inner').innerHTML += '<form> Post Content: <input style="margin-left:23px;" type="text" id="postText"></br><button id="send" type="button" onclick="updatePost('+type+', '+id+')">Enter</button></form>';
    if(type==1) document.getElementById('postText').value = document.getElementById("post_content_"+id).innerHTML;
    if(type == 3) document.getElementById('postText').value = document.getElementById("comment_content_"+id).innerHTML;
}
function updatePost(type, id){
    let postText = document.getElementById('postText');
    switch(type){
        case 1: executeRequest("api/v1/comments/", 'PUT', JSON.stringify({"id": id, "content": postText.value}), headers); break;
        case 2: break;
        case 3: executeRequest("api/v1/posts/", 'PUT', JSON.stringify({"id": id, "content": postText.value}), headers); break;
        default: break;
    }
    document.getElementById('overlay_inner').innerHTML = '<h3 style="margin:0 auto;">Edit Complited. Update this web-page to see changes.</h3><br/><button class="reloadBtn" onclick="document.location.reload()"></button>';  
}
//Create
function createPostButton(type, id){
    console.log("1")
    drawOverlay();
    document.getElementById('overlay_inner').innerHTML += '<form> Post Content: <input style="margin-left:23px;" type="text" id="postText"></br><button id="send" type="button" onclick="createPost('+type+', '+id+')">Enter</button></form>';
}
function createPost(type, id = null){
    headers = {"Content-Type" : "application/json","Authorization" : "Token "+window.localStorage.getItem("token")};
    switch(type){
        case 1: executeRequest("api/v1/comments/", 'POST', JSON.stringify({"post": id,"content": postText.value}), headers); console.log(JSON.stringify({"post": id,"content": postText.value})); break;
        case 2: break;
        case 3: executeRequest("api/v1/posts/", 'POST', JSON.stringify({"content": postText.value}), headers); break;
        default: break;
    }
    document.getElementById('overlay_inner').innerHTML = '<h3 style="margin:0 auto;">Update this web-page to see changes.</h3><br/><button class="reloadBtn" onclick="document.location.reload()"></button>';
}
//Login
function loginButton(){ 
    drawOverlay();
    document.getElementById('overlay_inner').innerHTML += '<form> Email: <input style="margin-left:23px;" type="text" id="email"><br/>Password: <input style="margin-left:23px;" type="text" id="password"></br><button id="send" type="button" onclick="login()">Enter</button></form>';
}
function login(){
    executeRequest("auth/token/login", 'POST', JSON.stringify({"email": document.getElementById('email').value, "password": document.getElementById('password').value}))
    .then(r => {window.localStorage.setItem('token', r['auth_token']); document.location.reload();});
}
//register
function registerButton(){
    drawOverlay();
    document.getElementById('overlay_inner').innerHTML += '<h3 style="margin:0 auto;">You will have to log in after confirming your email.</h3><br/><form> Email: <input style="margin-left:23px;" type="text" id="email"><br/>Username: <input style="margin-left:23px;" type="text" id="username"><br/>Password: <input style="margin-left:23px;" type="text" id="password"></br><button id="send" type="button" onclick="register()">Enter</button></form>';
}
function register(){
    executeRequest("auth/users", 'POST', JSON.stringify({"username" : document.getElementById('username').value, "email": document.getElementById('email').value, "password": document.getElementById('password').value}))
    .then(() => {document.getElementById('overlay_inner').innerHTML = '<h3 style="margin:0 auto;">Confirm your email</h3><br/><button class="toLoginFormButton" onclick="loginButton()"> Login Form </button>'})
}
//logout
function logoutButton(){
    executeRequest("auth/token/logout", 'POST', null, {"Authorization" : "Token "+window.localStorage.getItem('token')})
    .then(() => {
        window.localStorage.removeItem('token');
        document.location.reload();
    });
}