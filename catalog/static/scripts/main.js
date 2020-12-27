// TODO: Fix message removing
const removingTimeout = 5000; // 1 seconds timeout
function removeMessages() {
    console.log("remove");
    let container = document.querySelector(".messages-container");
    while(container.firstChild) {
        container.removeChild(container.firstChild);
    }
}
removeMessages();
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
    const navigationClass = navigation.getAttribute("class");
    // TODO: Repair showing
    button.onclick = () => {
        console.log("click", navigation.style.visibility.valueOf());
        let navigationShown = navigation.style.display !== "none";
        if(navigationShown) {
            // User sees navigation, now make it invisible
            navigation.style.display = "none";
        }
        else {
            navigation.style.display = navigationDisplay;
        }
    }
})();