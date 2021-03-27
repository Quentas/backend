function getMe(){
    try{
        var token = window.localStorage.getItem("token");
        const url = "https://fierce-dusk-92502.herokuapp.com/auth/users/me";
        const response = fetch(url, {
            method : 'GET',
            body : null,
            headers : {
                "Content-Type" : "application/json",
                "Authorization" : "Token "+token
            }
        }); 
        return response.json();
    }
    catch{
        console.log("Couldn't get user info.")
    }
}

function fillPostDefaultTemplate(postJSON, userJSON){
    let editBtnHTML = '';
    //if(postJSON['user'] = ME['user'])
    //    editBtnHTML = '<button class="edit_btn" onclick="updatePostButton('+postJSON['id']+')">Edit Post</button>';
    return '<div class="post" id="postID_'+postJSON['id']+'"> <div class="authorBlock"> <img class="authorAvatar" src="'+userJSON['profile_photo']+'" alt="profile photo"> <div class="authorBlock__inner"> <div class="authorName">'+userJSON['username']+'</div> <time class="datePosted">'+formatDate(new Date(postJSON['date']).toString())+'</time> </div> </div> <div id="post_content_'+postJSON['id']+'" class="contentBlock">'+postJSON['content']+'</div> <div class="other"> <button id="commentsBtn_'+postJSON['id']+'" class="comment_btn" onclick="showComments('+postJSON['id']+')">Comments</button>' + editBtnHTML +' </div> <div class="commentsBlock" id="commentsBlock_'+postJSON['id']+'"> </div> </div>';
}

function fillCommentDefaultTemplate(commentJSON, userJSON){
    return '<div class="authorBlock"> <img class="authorAvatar" src="'+userJSON['profile_photo']+'" alt="profile photo"> <div class="authorBlock__inner"> <div class="authorName">'+userJSON['username']+'</div> <time class="datePosted">'+commentJSON['date']+'</time> </div> </div> <div class="contentBlock">'+commentJSON['content']+'</div>';
}

function formatDate(date){
    function pad(s) { return (s < 10) ? '0' + s : s; }
    var d = new Date(date)
    return pad(d.getDate()) + "/" + pad(d.getMonth()+1) + "/" + d.getFullYear() + "/ " + pad(d.getHours())+":"+ pad(d.getMinutes());
}

function showComments(id){
    let intervalCounter = 0;
    let comments = [];
    let users = [];
    let commentsJSON = [];
    let usersJSON = [{"id":0}];
    let commentsCounter = 0;
    let usersCounter = 0;

    getComments(id).then(comJSON => {
        commentsCounter = comJSON.length;
        comJSON.forEach(com => {
            commentsJSON.push(com);
            users.push(com['user']);
        });
    });

    let t = setInterval(function(){
        console.log("waiting for comments " + commentsJSON.length +"/"+ commentsCounter)
        if(commentsCounter == 0 && intervalCounter > 20) clearInterval(t);
        if(commentsJSON.length == commentsCounter && commentsCounter != 0){
            users = [...new Set(users)];
            console.log("comments have loaded")
            users.forEach(user => {
                getUser(user).then(userJSON => {
                    usersJSON[user] = userJSON;
                    usersCounter++;
                });
            });
            clearInterval(t);
            let g = setInterval(function(){
                console.log("waiting for users " + usersCounter +"/"+users.length)
                if(users.length == usersCounter && usersCounter != 0){
                    console.log("users have loaded")
                    commentsJSON.forEach(comment => {
                        comments.push({"id" : comment['id'], "comment" : fillCommentDefaultTemplate(comment, usersJSON[comment['user']])});
                    })
                    clearInterval(g);
                    let n = setInterval(function(){
                        console.log("waiting for comments confirmation " + comments.length +"/"+commentsCounter)
                        if(comments.length == commentsCounter){
                            console.log("comments confirmed")
                            comments.sort((a,b)=> b.id - a.id);
                            comments.forEach(comment=>{
                                document.getElementById('commentsBlock_'+id).innerHTML += comment['comment'];     
                            });
                            document.getElementById('commentsBtn_'+id).onclick = "";
                            document.getElementById('commentsBtn_'+id).addEventListener('click', () => {
                                if(document.getElementById('commentsBlock_'+id).style.display == "block")
                                    document.getElementById('commentsBlock_'+id).style.display = "none";
                                else
                                    document.getElementById('commentsBlock_'+id).style.display = "block";
                
                            });
                            document.getElementById('commentsBtn_'+id).click()
                        clearInterval(n);
                        }
                    }, 10);
                }
            }, 10);
        }
        intervalCounter++;
    }, 10);
}



async function getPostsNumber(){
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/";
    const response = await fetch(url);
    return await response.json().length;
}

async function getPost(id){
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/"+id;
    const response = await fetch(url); 
    return await response.json();
}

async function getUser(id){
    const url = "https://fierce-dusk-92502.herokuapp.com/auth/users/"+id;
    const response = await fetch(url); 
    return await response.json();
}

async function getComments(id){
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/comments/?post_id="+id;
    const response = await fetch(url); 
    return await response.json();
}

function loadPostsFromTo(startpos, endpos){
    console.log(startpos, endpos)
    var l = new XMLHttpRequest();
    l.open("GET", "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/?startpos="+startpos+"&endpos="+endpos, true);
    l.setRequestHeader('Content-Type', 'application/json');
    l.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            let posts = [];
            let postsIDs = JSON.parse(l.responseText);
            let users = [];
            let postsJSON = [];
            let usersJSON = [{"id":0}];
            console.log(postsIDs)
            postsIDs.forEach(id => {
                getPost(id['id']).then(postJSON => {
                    postsJSON.push(postJSON);
                    users.push(postJSON['user']);
                });
            });
            let usersCounter = 0;
            let t = setInterval(function(){
                console.log("waiting for posts " + postsJSON.length +"/"+postsIDs.length)
                if(postsIDs.length == postsJSON.length){
                    users = [...new Set(users)];
                    console.log("posts have loaded")
                    users.forEach(user => {
                        getUser(user).then(userJSON => {
                            usersJSON[user] = userJSON;
                            usersCounter++;
                        });
                    });
                    clearInterval(t);
                    let g = setInterval(function(){
                        console.log("waiting for users " + usersCounter +"/"+users.length)
                        if(users.length == usersCounter && usersCounter != 0){
                            console.log("users have loaded")
                            postsJSON.forEach(post => {
                                posts.push({"id" : post['id'], "post" : fillPostDefaultTemplate(post, usersJSON[post['user']])});
                            })
                            clearInterval(g);
                            let n = setInterval(function(){
                                console.log("waiting for posts confirmation " + posts.length +"/"+postsIDs.length)
                                if(postsIDs.length == posts.length){
                                    console.log("posts confirmed")
                                    posts.sort((a,b) => b.id - a.id);
                                    posts.forEach(post => {
                                        document.querySelector('main').innerHTML += post['post'];        
                                    });
                                clearInterval(n);
                                }
                            }, 10);
                        }
                    }, 10);
                }
            }, 10);
        }
    }
    l.send();
}

function loadPosts(){
    let postsNumber = getPostsNumber();
    console.log(postsNumber)
    let startpos = 0;
    let endpos = 5;
    function f(){
        loadPostsFromTo(startpos, endpos);
        startpos = endpos;
        if(endpos + 5 > postsNumber) endpos = postsNumber;
        else endpos += 5;
    }
    f();
    let lastPageYOffset = 0;
    window.addEventListener('scroll', function() {
        if(pageYOffset - lastPageYOffset >= 1250){
            if(endpos < postsNumber){
                f();
            }else{
                console.log("All posts were loaded.");
                // remove Event Listener
            }
        }
    });
}

let ME = getMe();
//document.getElementById('myInfo').innerHTML = '<img src='+ME['profile_photo']+'>'+ ME['username']+'';

loadPosts()