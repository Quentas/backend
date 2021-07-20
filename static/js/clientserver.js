
function registration(){
    let username = document.getElementById("reg_username").value;
    let email =  document.getElementById("reg_email").value;
    let password =  document.getElementById("reg_pass").value;
    let re_password =  document.getElementById("reg_repass").value;
    if(password == re_password)
        executeRequest("auth/users/", 'POST', {
            "username": username,
            "password": password,
            "re_password": re_password,
            "email": email
        }, {"Content-Type" : "application/json", "Accept": "application/json"}).then(r => console.log(r))
    else{
        alert("Passwords do not match")
    }
}

function login(){
    let password = document.getElementById("login_pass").value;
    let email =  document.getElementById("login_email").value;
    executeRequest("auth/token/login/", 'POST', {
        "password": password,
        "email": email
    }, {"Content-Type" : "application/json", "Accept": "application/json"}).then(r => {
        console.log(r);
        window.localStorage.setItem('token', r['auth_token']);
        document.location.reload();
    })
}


let inputSearch = document.getElementById("searchInput");
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
    if(post) b = document.getElementById('likeBtn_' + postID);
    else b = document.getElementById('likeBtn__isComment_' + postID);
    if(!b.classList.contains("active")){
        b.classList.toggle("active");
        b.textContent = Number.parseInt(b.textContent) + 1;
        //send to server
    }
    else{      
        b.classList.toggle("active");
        b.textContent = Number.parseInt(b.textContent) - 1;
        //send to server
    }
}

function repostPost(postID, post){
    let b;
    if(post) b = document.getElementById('repostBtn_' + postID);
    else b = document.getElementById('repostBtn__isComment_' + postID);
    if(!b.classList.contains("active")){
        b.classList.toggle("active");
        b.textContent = Number.parseInt(b.textContent) + 1;
        //send to server
    }
    else{      
        b.classList.toggle("active");
        b.textContent = Number.parseInt(b.textContent) - 1;
        //send to server
    }
}

function addToBookmark(postID, post){
    let b;
    if(post) b = document.getElementById('addToBookmarkBtn_' + postID);
    else b = document.getElementById('addToBookmarkBtn__isComment_' + postID);
    if(!b.classList.contains("active")){
        b.classList.toggle("active");
        //send to server
    }
    else{      
        b.classList.toggle("active");
        //send to server
    }
}

function createComment(){

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


