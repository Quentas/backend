// ***   SERVER-CLIENT LOGIC   ***


loaderStarter()
function loaderStarter(){
    let s = 0, e = 10;
    function loader(){
        let postsJSON = [], posts = [];
        executeRequest("api/v1/posts/?startpos="+s+"&endpos="+e, 'GET') // get ids from s to e
        .then(postsJSONs => {
            if(postsJSONs.length != 0){
                //document.getElementById('loadingAnimation_1').style.display = 'block';
                postsJSONs.forEach(postJSON => {
                    postsJSON.push(postJSON);
                    if(postsJSON.length == postsJSONs.length) // starts after all post have been loaded
                        postsJSONs.forEach(postJSON => {
                            posts.push({"id" : postJSON['id'], "postHTML" : fillPostHTML("post", postJSON)});
                            if(posts.length == postsJSONs.length){
                                posts.sort((a,b) => b.id - a.id);
                                let f = document.getElementById('feed');
                                posts.forEach(post => {
                                    f.innerHTML += post['postHTML'];
                                });
                                //document.getElementById('loadingAnimation_1').style.display = 'none';
                            }
                        });
                })
            }
        });
        s = e;
        e += 5;
    }
    loader();
    let lastPageYOffset = 0;
    window.addEventListener('scroll', function k() {
        if(pageYOffset - lastPageYOffset >= 90){
            if(loader()) window.removeEventListener('scroll', k);
            lastPageYOffset = pageYOffset;
        }
    });
}



// HOW TO GET NEWPOSTCOUNTER => WRITE LENGHT OF POSTS ON START => EVERY MINUTE GET THE NEW LENGHT => COMPARE THEM => RESULT GOES TO NEWPOSTCOUNTER VARIAEBLE



let NotificationsNumber = 15; // get
let newPostsCounter = 19 // get

// ***   LOADING LOGIC   ***

console.log(window.localStorage.getItem('token'))

if(newPostsCounter == 0)
    document.getElementById("showNewPostsButton").style.display = "none";
else
    document.getElementById("newPostsCounter").textContent = newPostsCounter;

let newNotifications = document.getElementById("NotificationsCounter");
if(NotificationsNumber == 0) newNotifications.style.display = "none";
else if(NotificationsNumber < 10){ newNotifications.style.padding = "1px 6px"; newNotifications.textContent = NotificationsNumber;}
else {newNotifications.style.padding = "1px 3px"; newNotifications.textContent = "9+";}


// ***   USER LOGIC   ***

document.getElementById("showNewPostsButton").addEventListener("click", () => {document.location.reload();}); // show new posts


