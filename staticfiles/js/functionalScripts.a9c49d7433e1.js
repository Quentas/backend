function drawWrapper(){
    document.querySelector('body').innerHTML +=  '<div id="pw" style="height:'+window.screen.availHeight + 'px; width:'+window.screen.availWidth + 'px"><button id="cb" onclick="removePW()">X</button><div id="pf"></div></div>';
}

function removePW(){
    document.getElementById("pw").remove();
}

function createPostButton(){
    drawWrapper();
    let pf = document.getElementById('pf');
    if(window.localStorage.getItem("token") != ""){
        pf.innerHTML += '<form>Post Content: <input style="margin-left:23px;" type="text" id="l"></br><button id="send" type="button" onclick="createPost()">Enter</button></form>';
        
    }
    else{
        pf.innerHTML += '<p>You are not loged in !</p><br/><button onclick="removePW()">Close</button>';
    }
}

function updatePostButton(id){
    drawWrapper();
    let pf = document.getElementById('pf');
    if(window.localStorage.getItem("token") != ""){
        pf.innerHTML += '<form> Post Content: <input style="margin-left:23px;" type="text" id="l"></br><button id="send" type="button" onclick="updatePost('+id+')">Enter</button></form>';
        let l = document.getElementById('l');
        l.value = document.getElementById("post_content_"+id).innerHTML;    
    }
    else{
        pf.innerHTML += '<p>You are not loged in !</p><br/><button onclick="removePW()">Close</button>';
    }
}

function loginButton(){
    drawWrapper();
    document.getElementById('pf').innerHTML += '<form> Email: <input style="margin-left:23px;" type="text" id="p"><br/>Password: <input style="margin-left:23px;" type="text" id="l"></br><button id="send" type="button" onclick="login()">Enter</button></form>';   
}

function registerButton(){
    drawWrapper();
    document.getElementById('pf').innerHTML += '<h3>You will have to log in after confirming your email.</h3><br/><form> Email: <input style="margin-left:23px;" type="text" id="p"><br/>Username: <input style="margin-left:23px;" type="text" id="u"><br/>Password: <input style="margin-left:23px;" type="text" id="l"></br><button id="send" type="button" onclick="register()">Enter</button></form>';   
}

function logoutButton(){
    drawWrapper();
    document.getElementById('pf').innerHTML += 'Are you sure you want to log out </br><button onclick="logout()">Yes</button><button onclick="removePW();">No</button>';  
}

function createPost(){
    let l = document.getElementById('l');
    var token = window.localStorage.getItem("token");
    const url = "http://127.0.0.1:8000/api/v1/posts/";
    const response = fetch(url, {
        method : 'POST',
        body : JSON.stringify({"content": l.value}),
        headers : {
            "Content-Type" : "application/json",
            "Authorization" : "Token "+token
        }
    });
    response.then(()=> {
        let pw = document.getElementById('pw');
        let b = document.createElement('button');
        b.className = "reloadBtn";
        b.addEventListener('click', ()=>{
            document.location.reload();
        })
        pw.append(b);
    });
    return 0;
}

function updatePost(id){
    let l = document.getElementById('l');
    var token = window.localStorage.getItem("token");
    const url = "http://127.0.0.1:8000/api/v1/posts/";
    const response = fetch(url, {
        method : 'PUT',
        body : JSON.stringify({"id": id, "content": l.value}),
        headers : {
            "Content-Type" : "application/json",
            "Authorization" : "Token "+token
        }
    });
    response.then(()=>{editEditedPost(id)});
    removePW();
    return 0;
}

async function login(){
    let p = document.getElementById('p');
    let l = document.getElementById('l');
    const url = "http://127.0.0.1:8000/auth/token/login";
    const response = await fetch(url, {
        method : 'POST',
        body : JSON.stringify({"email": p.value, "password": l.value}),
        headers : {
            "Content-Type" : "application/json"
        }
    });
    await response.json().then(r => {window.localStorage.setItem('token', r['auth_token']); document.location.reload();});
    removePW();
    return 0;
}

function register(){
    let u = document.getElementById('u');
    let p = document.getElementById('p');
    let l = document.getElementById('l');
    const url = "http://127.0.0.1:8000/auth/users";
    const response = fetch(url, {
        method : 'POST',
        body : JSON.stringify({"username" : u.value, "email": p.value, "password": l.value}),
        headers : {
            "Content-Type" : "application/json"
        }
    });
    removePW();
    createPost();
    return 0;
}

function logout(){
    let token = window.localStorage.getItem('token');
    const url = "http://127.0.0.1:8000/auth/token/logout";
    const response = fetch(url, {
        method : 'POST',
        body : null,
        headers : {
            "Authorization" : "Token "+token
        }
    });
    window.localStorage.removeItem('token');
    document.location.reload();
    return 0;

}

function editEditedPost(id){
    getPost(id).then(postJSON => {
        document.getElementById('post_content_'+id).innerText = postJSON['content'];
        document.getElementById('datePosted_'+id).innerHTML = '<div id="datePosted_'+postJSON['id']+'" class="datePosted">'+formatDate(new Date(postJSON['date']).toString())+' (last edited: '+ formatDate(new Date(postJSON['last_edited']).toString()) +')</div>';
    });
}