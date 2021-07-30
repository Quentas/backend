// ***   SERVER-CLIENT LOGIC   ***



loaderStarter()
function loaderStarter(){
    let s = 0, e = 10;
    function loader(){
        let postsJSON = [], posts = [];
        axios.get(url + "api/v1/posts/?startpos="+s+"&endpos="+e) // get ids from s to e
        .then(postsJSONs => {
            if(postsJSONs.length != 0){
                postsJSONs.data.forEach(postJSON => {
                    console.log(postsJSONs.data.length)
                    postsJSON.push(postJSON);
                    if(postsJSON.length == postsJSONs.data.length){
                        console.log(postsJSON)
                        postsJSONs.data.forEach(postJSON => {
                            posts.push({"id" : postJSON['id'], "postHTML" : fillPostHTML("post", postJSON)});
                            if(posts.length == postsJSONs.data.length){
                                posts.sort((a,b) => b.id - a.id);
                                let f = document.getElementById('feed_subscriptions');
                                posts.forEach(post => {
                                    f.innerHTML += post['postHTML'];
                                    updateImages(post['id']);
                                });
                            }
                        });
                    }
                    /*
                    postsJSON.push(postJSON);
                    if(postsJSON.length == postsJSONs.length) // starts after all post have been loaded
                        postsJSONs.forEach(postJSON => {
                            posts.push({"id" : postJSON['id'], "postHTML" : fillPostHTML("post", postJSON)});
                            if(posts.length == postsJSONs.length){
                                posts.sort((a,b) => b.id - a.id);
                                let f = document.getElementById('feed_subscriptions');
                                posts.forEach(post => {
                                    f.innerHTML += post['postHTML'];
                                    updateImages(post['id']);
                                });
                            }
                        });
                        */
                })
            }
        }).catch(err => console.log(err));
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


Overlay.style.height = (window.innerHeight + 100) + "px";
window.addEventListener('resize', function(event) {
    Overlay.style.minHeight = (window.innerHeight + 1) + "px";
    if(openedImage.children[0].height + 201 > window.innerHeight){
        Overlay.style.height = (openedImage.children[0].height + 201) +"px";
        Overlay.classList.remove("fixed");
    } 
    else Overlay.classList.add("fixed");
});

function loadImages(event) {
    for(let i = 0; i < event.target.files.length; i++)
        if (newPostImages.childElementCount < 6 && i < 6){
            document.getElementById('newPostImages').innerHTML += '<div class="newPostImage" onclick="openImage(event, this)" style="background-image: url(' + URL.createObjectURL(event.target.files[i]) + ')"><button class="removeImageBtn" onclick="this.parentElement.remove(); updateImages(0.1);">X</button></div>';
            updateImages("n");   
        }
        else break; 
};

function updateImages(x, o = null){
    let PostImages = Number.isInteger(x) ? document.getElementById('postImages_'+x) : document.getElementById('newPostImages');
    if(o == "o") PostImages = document.getElementById('openedPostImages_'+x)
    if(PostImages.childElementCount > 0)
        Array.from(PostImages.children).forEach(child => {
            PostImages.classList.remove("n_0", "n_1", "n_2", "n_3", "n_4", "n_5", "n_6");
            child.classList.remove("n_0", "n_1", "n_2", "n_3", "n_4", "n_5", "n_6");
            PostImages.classList.add("n_" + (PostImages.childElementCount));
            child.classList.add("n_" + (PostImages.childElementCount));
        });
    else{
        PostImages.classList.add("n_0");
    }
}



function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}


var scrollDiv = document.createElement("div");
scrollDiv.className = "scrollbar-measure";
document.body.appendChild(scrollDiv);
var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;
pageWrapper__Overlay.style.right = scrollbarWidth+"px";
document.body.removeChild(scrollDiv);