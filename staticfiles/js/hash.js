Overlay.addEventListener("click", (e) => {
    if(e.target === Overlay && EngageHolder.classList.contains("innactive")){ OverlayBackLogic(); pageWrapper__Overlay.classList.remove("fixed");}
});

function OverlayBackLogic(){
    openedImage.innerHTML = "";
    if(!Login.classList.contains("innactive")){
        Login.classList.add("innactive");
        Registration.classList.remove("innactive");
        if(!(document.location + "").includes("/reg")) history.pushState("", "", "/registration");
    }
    else if(!Forgot.classList.contains("innactive")){
        Forgot.classList.add("innactive");
        Login.classList.remove("innactive");
        if(!(document.location + "").includes("/log")) history.pushState("", "", "/login");
    }
    else{
        body.classList.remove("noscroll");
        Overlay.classList.add("innactive");
        Registration.classList.add("innactive");
        Login.classList.add("innactive");
        openedPost.classList.add("innactive");
        Forgot.classList.add("innactive");
        document.getElementById("Logout").classList.add("innactive");  
        history.pushState("", "", "")
    }
}

window.addEventListener('hashchange', loadHash);
loadHash();
function loadHash(){
    let current = (document.location+"").split('/');
    console.log(current)
    try{
        switch(current[1][0]){
            case 'r': openRegisterForm(); break;
            case 'l': openLoginForm(); break;
            case 'f': openForgotForm(); break;
            case 'p': showPost(current[2]); break;
            case '': Overlay.classList.add("innactive"); Profile.classList.add("innactive"); feed_subscriptions.classList.remove("innactive"); pageWrapper__Overlay.classList.remove("fixed"); break;
            case 'u': openProfile(current[2]); break;
            case 'm': openImage(); break;
            default:  break;
        }
    }catch (err){
        Overlay.classList.add("innactive"); feed_subscriptions.classList.remove("innactive"); Profile.classList.add("innactive"); pageWrapper__Overlay.classList.remove("fixed");
    }
        
}

function showPost(e, postID){
    if(!e.target.classList.contains("Username") && !e.target.classList.contains("comment_btn") && !e.target.classList.contains("repost_btn") && !e.target.classList.contains("like_btn") && !e.target.classList.contains("addToBookmark_btn") && !e.target.classList.contains("postImage") && !e.target.classList.contains("other")){
        pageWrapper__Overlay.classList.add("fixed");
        Overlay.classList.remove("innactive");
        Overlay.style.background = "rgba(0, 0, 0, .65)";
        EngageHolder.classList.add("innactive");
        openedPost.classList.remove("innactive");
        Registration.classList.add("innactive");
        Login.classList.add("innactive");
        Forgot.classList.add("innactive");
        if(lastOpenedPost == ""){
            axios.get(url + "api/v1/posts/"+postID).then(
                postJSON => {
                    document.getElementById("openedPostContent").innerHTML += document.getElementById("post_"+postID).innerHTML.replace("postImages_", "openedPostImages_").replace("commentsBtn_", "openedCommentsBtn_").replace("repostBtn_", "openedRepostBtn_").replace("likeBtn_", "openedLikeBtn_").replace("addToBookmarkBtn_", "openedAddToBookmarkBtn_");
                    updateImages(postJSON['id'], "o");
                    for(let i = 0; i < postJSON['comments_count']; i++){
                        document.getElementById("openedPostComments").innerHTML += fillPostHTML("comment", postJSON['comments'][i]);
                    }
                }
            )
        }
        else if(lastOpenedPost != postID){
            document.getElementById("openedPostComments").innerHTML = "";
            document.getElementById("openedPostContent").innerHTML = document.getElementById("post_"+postID).innerHTML.replace("postImages_", "openedPostImages_").replace("commentsBtn_", "openedCommentsBtn_").replace("repostBtn_", "openedRepostBtn_").replace("likeBtn_", "openedLikeBtn_").replace("addToBookmarkBtn_", "openedAddToBookmarkBtn_");
            updateImages(postID, "o");
            axios.get(url + "api/v1/posts/"+postID).then(
                postJSON => {
                    for(let i = 0; i < postJSON['comments_count']; i++){
                        document.getElementById("openedPostComments").innerHTML += fillPostHTML("comment", postJSON['comments'][i]);
                    }
                }
            )
        }
        else{}
        lastOpenedPost = postID;
        history.pushState("", "", "/post/"+postID);

    }
}


function openRegisterForm(){
    body.classList.add("noscroll");
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");

    openedPost.classList.add("innactive");
    Registration.classList.remove("innactive");
    Login.classList.add("innactive");
    Forgot.classList.add("innactive");
    if(!(document.location + "").includes("/reg")) history.pushState("", "", "/registration");
}

function openLoginForm(){
    body.classList.add("noscroll");
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");

    openedPost.classList.add("innactive");
    Registration.classList.add("innactive");
    Login.classList.remove("innactive");
    Forgot.classList.add("innactive");
    if(!(document.location + "").includes("/log")) history.pushState("", "", "/login");
}

function openForgotForm(){
    body.classList.add("noscroll");
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");
    
    openedPost.classList.add("innactive");
    Registration.classList.add("innactive");
    Login.classList.add("innactive");
    Forgot.classList.remove("innactive");
    if(!(document.location + "").includes("/for")) history.pushState("", "", "/forgotPassword");
}

function openImage(e, imgBlob){
    if(!e.target.classList.contains("removeImageBtn")){
        pageWrapper__Overlay.classList.add("fixed");
        Overlay.classList.remove("innactive");
        Overlay.style.background = "rgba(0, 0, 0, .65)";
        EngageHolder.classList.add("innactive");
        openedImage.classList.remove("innactive");
        openedImage.innerHTML += '<img class="openedImage" src="'+imgBlob.style.backgroundImage.slice(5,-2)+'">';
        openedImage.style.height = document.getElementsByClassName('openedImage')[0].height + "px";
        if(openedImage.children[0].height + 201 > window.innerHeight){
            Overlay.classList.remove("fixed");
            Overlay.style.height = (openedImage.children[0].height + 201) +"px";
        }else{
            Overlay.classList.add("fixed");
            Overlay.style.height = (window.innerHeight + 100) + "px";
        }
        if(!(document.location + "").includes("/med")) history.pushState("", "", ""+openedImage.children[0].src);
    }else{}
}

function openProfile(user){
    console.log(user)
    if(lastOpenedUser == ""){
        axios.get(url + "auth/users/"+user).then(
            userJSON => {
                Profile.innerHTML += fillPostHTML("post", userJSON);
                //for(let i = 0; i < userJSON['posts']; i++){}
            }
        )
    }
    else if(lastOpenedUser != user){
        Profile.innerHTML = "";
        axios.get(url + "auth/users/"+user).then(
            userJSON => {
                Profile.innerHTML += fillPostHTML("post", userJSON);
                //for(let i = 0; i < userJSON['posts']; i++){}
            }
        )
    }
    lastOpenedUser = user;
    Profile.classList.remove("innactive");
    feed_subscriptions.classList.add("innactive")
    if(!(document.location + "").includes("/use")) history.pushState("", "", "/user/"+user);
}

