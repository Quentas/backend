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

function updatePostButton(){
    drawWrapper();
    let pf = document.getElementById('pf');
    if(window.localStorage.getItem("token") != ""){
        pf.innerHTML += '<form> ID: <input style="margin-left:23px;" type="text" id="p"><br/>Post Content: <input style="margin-left:23px;" type="text" id="l"></br><button id="send" type="button" onclick="updatePost()">Enter</button></form>';
        
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

function createPost(){
    let l = document.getElementById('l');
    var token = window.localStorage.getItem("token");
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/";
    const response = fetch(url, {
        method : 'POST',
        body : JSON.stringify({"content": l.value}),
        headers : {
            "Content-Type" : "application/json",
            "Authorization" : "Token "+token
        }
    });
    removePW();
    return 0;
}

function updatePost(){
    let p = document.getElementById('p');
    let l = document.getElementById('l');
    var token = window.localStorage.getItem("token");
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/";
    const response = fetch(url, {
        method : 'PUT',
        body : JSON.stringify({"id": p.value, "content": l.value}),
        headers : {
            "Content-Type" : "application/json",
            "Authorization" : "Token "+token
        }
    });
    removePW();
    return 0;
}

function login(){
    let p = document.getElementById('p');
    let l = document.getElementById('l');
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/";
    const response = fetch(url, {
        method : 'POST',
        body : JSON.stringify({"email": p.value, "password": l.value}),
        headers : {
            "Content-Type" : "application/json"
        }
    });
    window.localStorage.setItem('token', response.json()['auth_token']);
    removePW();
    return 0;
}

function register(){
    let u = document.getElementById('u');
    let p = document.getElementById('p');
    let l = document.getElementById('l');
    const url = "https://fierce-dusk-92502.herokuapp.com/api/v1/posts/";
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