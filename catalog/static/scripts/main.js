const removingTimeout = 2000;
function removeMessages() {
    let container = document.querySelector(".messages-container");
    while(container.firstChild) {
        container.removeChild(container.firstChild);
    }
}
// Remove messages when all DOM has been loaded
document.addEventListener("DOMContentLoaded",() => {
    setTimeout(removeMessages, removingTimeout);
});
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
(function addNavigationRollingButtonOnclick() {
    const button = document.querySelector(".navigation-rolling-button");
    const navigation = document.querySelector(".navigation");
    // TODO: Repair showing
    button.onclick = () => {
        navigation.classList.toggle("navigation-hidden");
    }
})();
(function addSearchButtonOnclick() {
    const button = document.querySelector(".search-button");
    // TODO: Implement onclick
    button.onclick = () => {
        const search = document.querySelector(".search-container input[type='search']");
        const searchQuery = search.value;
        // Redirect to 'search' page
        const location = "/djangolearn/search/" + searchQuery;
        window.location.href = location;
    }
})();