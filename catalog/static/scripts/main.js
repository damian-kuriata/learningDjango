const removingTimeout = 1000; // 5 seconds timeout
document.onload = () => {
    console.log("onload");
    setTimeout(removeMessages, removingTimeout);
}
function removeMessages() {
    let container = document.querySelector(".messages-container");
    while(container.firstChild) {
        container.removeChild(container.firstChild);
    }
}
(function setSearchButtonOnclick() {
    let searchButton = document.querySelector(".search-button");
    searchButton.onclick = () => {
        let searchBox = document.querySelector(".search-container input[type='search']");
        let searchQuery = searchBox.value;
        const targetUrl = `/catalog/search/${ searchQuery }`;
        window.location.href = targetUrl;
    }
})()
// Function which escapes HTML characters (turns them into secure equivalent)
// & becomes &amp;< becomes &lt;> becomes &gt;" becomes &quot;'becomes &#39
// Returns html-escaped string
function escapeHtml(text) {
    text = text.replace('&', "&amp");
    text = text.replace('<', "&lt");
    text = text.replace('>', "&GT");
    text = text.replace('"', "&quot");
    text = text.replace("'", "&#39");
    return text;
}
function getWrittenComment() {
    const commentInput = document.querySelector("#comment-input");
    let comment = escapeHtml(commentInput.value);
    commentInput.value = '';
    return comment
}
function commentValid(comment) {
    return comment !== ''
}
function addNewCommentToPage(comment, user) {
    const commentsContainer = document.querySelector(".comments-container");
    let newCommentParagraph = document.createElement("p");
    const html_ = `<a href=${ user.absolute_url }>${ user.username }</a> wrote: ${ comment.comment }`;
    newCommentParagraph.innerHTML = html_;
    commentsContainer.appendChild(newCommentParagraph);
    // Add new flash message
    const message = "New comment successfully added";
    let messagesContainer = document.querySelector(".messages-container");
    let messageParagraph = document.createElement("p");
    messageParagraph.setAttribute("class", "message-info");
    messageParagraph.textContent = message;
    messagesContainer.appendChild(messageParagraph);
    setTimeout(removeMessages, removingTimeout);
}
function getCookie(name) {
    let cookieValue = null;
    if(document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for(let i=0; i<cookies.length; i++) {
            let cookie = cookies[i].trim();
            if(cookie.substring(0, name.length+1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function sendWrittenCommentToServer() {
    let comment = {"comment": getWrittenComment()};
    if(!commentValid()) {
        return;
    }
    const targetUrl = "add-comment/";
    // Website is CSRF-protected, CSRF token (named 'csrftoken') must be sent in AJAX in order to
    // Communicate with server, otherwise 403 HTTP Error is returned.
    const csrftoken = getCookie("csrftoken");
    let dataJson = JSON.stringify(comment);
    const init = {
        method: "POST",
        mode: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Content-Length": dataJson.length.toString(),
            'X-CSRFToken': csrftoken
        },
        body: dataJson,
        credentials: "same-origin"
    }
    fetch(targetUrl, init).then(response => {
        // As a response, server should return json like {"username": <username>}, where <username>
        // Is a name of user who wrote comment which contents were sent.
        return response.json();
    }).then(user => {
        addNewCommentToPage(comment, user)
    }).catch(error => {
        console.log(error);
    });

}
(function setWriteButtonOnClick() {
    console.log("clock")
    const writeButton = document.querySelector("#writeButton");
    writeButton.onclick = sendWrittenCommentToServer;
})();
function getPostingData(postingUrl) {
    let selectedImages = document.querySelectorAll(".images-pane input[type='checkbox']:checked");
    console.log(selectedImages);
    let postingData = '';
    for(let selectedImage of selectedImages) {
        postingData += (selectedImage.value.trim() + ';');
    }
    return postingData;
}
(function setGoButtonOnClick() {
    console.log("click");
    const goButton = document.querySelector("#go-button");
    goButton.onclick = () => {
        console.log("click");
        const options = document.querySelector("#options");
        if(options.value === "delete") {
            const csrftoken = getCookie("csrftoken");
            const postingUrl = "/catalog/delete-image-multiple";
            let postingData = getPostingData(postingUrl);
            const init = {
                 method: "DELETE",
                 mode: "same-origin",
                 headers: {
                    "Content-Type": "text/html",
                    "Accept": "application/json",
                    "Content-Length": postingData.length.toString(),
                    'X-CSRFToken': csrftoken
                 },
                 body: postingData,
                 credentials: "same-origin"
            }
            fetch(postingUrl, init).then((response) => {
                return response.json();
            }).then((data) => {
                console.log(data);
            })
        }

    }
})();