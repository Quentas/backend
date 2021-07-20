let Overlay = document.getElementById("Overlay");
Overlay.style.height = screen.height + "px";
let EngageHolder = document.getElementById("EngageHolder");
let Login = document.getElementById("Login");
let Registration = document.getElementById("Registration");
let openedPost = document.getElementById("openedPost");
let Forgot = document.getElementById("Forgot");
let lastOpenedPost = "";
let startLocation = (document.location + "").split('#')[0];

Overlay.addEventListener("click", (e) => {
    if(e.target === Overlay && EngageHolder.classList.contains("innactive")) OverlayBackLogic();
});

function OverlayBackLogic(){
    if(!Login.classList.contains("innactive")){
        Login.classList.add("innactive");
        Registration.classList.remove("innactive");
        if(!(document.location + "").includes("#r")) document.location = startLocation + "#r";
    }
    else if(!Forgot.classList.contains("innactive")){
        Forgot.classList.add("innactive");
        Login.classList.remove("innactive");
        if(!(document.location + "").includes("#l")) document.location = startLocation + "#l";
    }
    else{
        Overlay.classList.add("innactive");
        Registration.classList.add("innactive");
        Login.classList.add("innactive");
        openedPost.classList.add("innactive");
        Forgot.classList.add("innactive");
        document.getElementById("Logout").classList.add("innactive");  
        history.pushState({foo: "bar"} , "page 2", " ")
    }
}

window.addEventListener('hashchange', loadHash);
loadHash();
function loadHash(){
    let current = (document.location+"").split('#')[1];
    try{
        switch(current[0]){
            case 'r': openRegisterForm(); break;
            case 'l': openLoginForm(); break;
            case 'f': openForgotForm(); break;
            case 'p': showPost(current.slice(2)); break;
            case '': Overlay.classList.add("innactive"); break;
            default:  break;
        }
    }catch (err){
        Overlay.classList.add("innactive");
    }
        
}

function showPost(postID){
    Overlay.classList.remove("innactive");
    Overlay.style.background = "rgba(0, 0, 0, .65)";
    EngageHolder.classList.add("innactive");
    openedPost.classList.remove("innactive");
    Registration.classList.add("innactive");
    Login.classList.add("innactive");
    Forgot.classList.add("innactive");
    if(lastOpenedPost == ""){
        executeRequest("api/v1/posts/"+postID, 'GET').then(
            postJSON => {
                document.getElementById("openedPostContent").innerHTML += fillPostHTML("post", postJSON);
                for(let i = 0; i < postJSON['comments_count']; i++){
                    document.getElementById("openedPostComments").innerHTML += fillPostHTML("comment", postJSON['comments'][i]);
                }
            }
        )
    }
    else if(lastOpenedPost != "p_"+postID){
        document.getElementById("openedPostComments").innerHTML = "";
        document.getElementById("openedPostContent").innerHTML = document.getElementById("post_"+postID).innerHTML;
        executeRequest("api/v1/posts/"+postID, 'GET').then(
            postJSON => {
                for(let i = 0; i < postJSON['comments_count']; i++){
                    document.getElementById("openedPostComments").innerHTML += fillPostHTML("comment", postJSON['comments'][i]);
                }
            }
        )
    }
    lastOpenedPost = "p_"+postID;
    document.location = startLocation + "#p_"+postID;
}


function openRegisterForm(){
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");

    openedPost.classList.add("innactive");
    Registration.classList.remove("innactive");
    Login.classList.add("innactive");
    Forgot.classList.add("innactive");
    if(!(document.location + "").includes("#r")) document.location = startLocation + "#r";
}

function openLoginForm(){
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");

    openedPost.classList.add("innactive");
    Registration.classList.add("innactive");
    Login.classList.remove("innactive");
    Forgot.classList.add("innactive");
    if(!(document.location + "").includes("#l")) document.location = startLocation + "#l";
}

function openForgotForm(){
    Overlay.style.background = "#FAF9FF";
    Overlay.classList.remove("innactive");
    EngageHolder.classList.remove("innactive");
    
    openedPost.classList.add("innactive");
    Registration.classList.add("innactive");
    Login.classList.add("innactive");
    Forgot.classList.remove("innactive");
    if(!(document.location + "").includes("#f")) document.location = startLocation + "#f";
}
