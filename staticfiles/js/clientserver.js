
let Me = "";
function getMe(){
    let token = window.localStorage.getItem('token');
    if(token != undefined){
        document.getElementById('myProfile').classList.remove('innactive');       
        document.getElementById('signup').classList.add('innactive');
        axios.get(url+"auth/users/me",{},{
            headers : {
                "Content-Type" : "application/json",
                "Authorization" : "Token "+window.localStorage.getItem("token")
            }
        })
        .then(r => {Me = r; console.log("USERS/ME: "+typeof(r));console.log(r); Profile.addEventListener("click", openProfile(Me));});
    }else{
        Me = "";
        //document.getElementById('myProfile').classList.add('innactive');       
        //document.getElementById('signup').classList.remove('innactive');
    }
        

}
getMe();

function registration(){
    let username = document.getElementById("reg_username").value;
    let email =  document.getElementById("reg_email").value;
    let password =  document.getElementById("reg_pass").value;
    let re_password =  document.getElementById("reg_repass").value;
    if(password == re_password)
        axios.post(url + "auth/users/", {
            "username": username,
            "password": password,
            "re_password": re_password,
            "email": email
        },{
            headers : {
                "Content-Type" : "application/json", "Accept": "application/json"
            }
        })
    else if(PopUp.classList.contains("active")) PopUp.firstChild.textContent = "Passwords still do not match (:";
    else{
        PopUp.classList.add("active");
        PopUp.firstChild.textContent = "Passwords do not match";
        setTimeout(function(){ PopUp.classList.remove("active"); }, 5000);
    }
}

function login(){
    let password = document.getElementById("login_pass").value;
    let email =  document.getElementById("login_email").value;

    axios.post(url + "auth/token/login", {
        "password": password,
        "email": email
    },{
        "Content-Type" : "application/json",
        "Accept": "application/json"
    })
    .then(r => {
        if(r['auth_token'] != undefined){
            window.localStorage.setItem('token', r['auth_token']);
            document.location = startLocation;
        }else if(PopUp.classList.contains("active"))PopUp.firstChild.textContent = "Wrong Email or Username Again (:";
        else{
            PopUp.classList.add("active");
            PopUp.firstChild.textContent = "Wrong Email or Username";
            setTimeout(function(){ PopUp.classList.remove("active"); }, 5000);
        }
    });
}

Exit.addEventListener("click", logout);
function logout(){
    axios.post(url + "auth/token/logout", {},{
        headers:{
            "Authorization" : "Token " + window.localStorage.getItem('token')
        }
    })
    .then(() => {
        window.localStorage.removeItem('token');
        document.location.reload();
    });
}

function createComment(){

}

function createPost(){
   axios.post(url + "api/v1/posts/", {
    "content": newPostInput.value
   },
   {headers : {
       "Authorization" : "Token "+window.localStorage.getItem("token")
    }})
   .then(r => console.log(r))
   .catch(err => console.log(err));
}

document.getElementById("searchButton").addEventListener("click", ()=>{
    alert(inputSearch.value)
    //send to server
});
inputSearch.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("searchButton").click();
  }
});

input = document.getElementById('newPostInput');
input.addEventListener('input', () => {
    let scroll_height = input.scrollHeight;
    input.style.height = scroll_height + "px";
})


function likePost(postID, post){
    let b;
    let c = "";
    if(post) { b = document.getElementById('likeBtn_' + postID); try{c = document.getElementById('openedLikeBtn_' + postID);}catch{} }
    else b = document.getElementById('likeBtn__isComment_' + postID);

    if(!b.classList.contains("active")){
        b.classList.add("active");
        b.textContent = Number.parseInt(b.textContent) + 1;
        if(c != ""){
            c.classList.add("active");
            c.textContent = Number.parseInt(c.textContent) + 1;
        }
        send(true);
    }else{
        b.classList.remove("active");
        b.textContent = Number.parseInt(b.textContent) - 1;
        if(c != ""){
            c.classList.remove("active");
            c.textContent = Number.parseInt(c.textContent) - 1;

        }
        send(false);
    }

    function send(action){

    }
}

function repostPost(postID, post){
    let b;
    let c = "";
    if(post) { b = document.getElementById('repostBtn_' + postID); try{c = document.getElementById('openedRepostBtn_' + postID);}catch{} }
    else b = document.getElementById('repostBtn__isComment_' + postID);

    if(!b.classList.contains("active")){
        b.classList.add("active");
        b.textContent = Number.parseInt(b.textContent) + 1;
        if(c != ""){
            c.classList.add("active");
            c.textContent = Number.parseInt(c.textContent) + 1;
        }
        send(true);
    }else{
        b.classList.remove("active");
        b.textContent = Number.parseInt(b.textContent) - 1;
        if(c != ""){
            c.classList.remove("active");
            c.textContent = Number.parseInt(c.textContent) - 1;

        }
        send(false);
    }

    function send(action){

    }
}

function addToBookmark(postID, post){
    let b;
    let c = "";
    if(post) { b = document.getElementById('addToBookmarkBtn_' + postID); try{c = document.getElementById('openedAddToBookmarkBtn_' + postID);}catch{} }
    else b = document.getElementById('addToBookmarkBtn__isComment_' + postID);

    if(!b.classList.contains("active")){
        b.classList.add("active");
        b.textContent = Number.parseInt(b.textContent) + 1;
        if(c != ""){
            c.classList.add("active");
            c.textContent = Number.parseInt(c.textContent) + 1;
        }
        send(true);
    }else{
        b.classList.remove("active");
        b.textContent = Number.parseInt(b.textContent) - 1;
        if(c != ""){
            c.classList.remove("active");
            c.textContent = Number.parseInt(c.textContent) - 1;

        }
        send(false);
    }

    function send(action){

    }
}

document.getElementById("profileBtn").addEventListener("click", () => {
    document.getElementById("profileBtn").classList.toggle("active");
    document.getElementById("profileDropdown").classList.toggle("active");
});

Array.from(document.getElementsByClassName("addToFriendsListButton")).forEach(button => {
    button.addEventListener("click", () => {
        button.classList.toggle("active");
    });
    //send to server
});


/* TODO

Open responds to comment
deal with account mess smile




*/


