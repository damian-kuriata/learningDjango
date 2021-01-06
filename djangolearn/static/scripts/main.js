import {getCookie, escapeHTML} from "./modules/utils.js";

function removeMessages() {
    let container = $(".messages-container").first();
    const animationDurationMs = 200;
    container.fadeOut(animationDurationMs, () => $(this).remove());
}
function addNavigationRollingButtonOnclick() {
    const button = $(".navigation-rolling-button");
    const navigation = $(".navigation");
    button.click(() => {
        // Show navigation when it's hidden and hide when shown
        // is(':hidden') checks display attribute, it becomes
        // true when display is none
        if(navigation.is(":hidden")) {
            console.log("hidden");
            navigation.show(300, () => {
                navigation.css("display", "flex")
            });
        }
        else {
            navigation.hide(300);
        }
    })
}
function addSearchButtonOnclick() {
    const button = $(".search-button");
    button.click(() => {
        const search = $(".search-container input[type='search']");
        const searchQuery = search.val();
        // Redirect to 'search' page
        const location = "/djangolearn/search/" + searchQuery;
        window.location.href = location;
    });
}
function createMessageParagraph(html, class_) {
        return $("</p>", {
            html: html,
            "class": class_
        })
}
function refreshList(list) {
    //let oldChildren = messagesContainer.not(`:nth-child(${index + 1})`);
    let children = list.children();
    list.empty();
    list.append(children);
}
function addAddButtonOnclick() {
    console.log("clicl");
    const button = $("#add-language-button");
    button.click(() => {
       const languageInput = $("#add-language-input");
       let languageName = languageInput.val().trim().toLowerCase();
       const requestUrl = `djangolearn/api/languages/${languageName}/`;
       const csrfToken = getCookie("csrftoken");
       const init = {
           method: "POST",
           mode: "same-origin",
           headers: {
               "X-CSRFToken": csrfToken
           }
       }
       fetch(requestUrl, init).then((response) => {
           return response.json();
       }).then((data) => {
           if(data.error) {
               let html = data.error;
               let class_ = "message-error";
               console.log(html);
               $(".messages-container").append(createMessageParagraph(html, class_));
           }
           if(data.success) {
               let html = data.success;
               console.log(html);
               let class_ = "message-info";
               // Refresh page
               window.location.href = window.location.href;
               const messagesContainer = $(".messages-container");

               messagesContainer.append(createMessageParagraph(html, class_));
               let oldChildren = messagesContainer.children();
               messagesContainer.empty();
               messagesContainer.append("test");
           }
       });
    });
}
function addDeleteLanguageButtonOnclicks() {
    const languagesList = $(".languages-list").find("li");
    //console.log(languagesList.find("span").eq(0).text("tesddst"));
    languagesList.find("div").each(function(index) {
        let children = $(this).children();
        let languageName = children.eq(0).text();
        let managePhrasesButton = children.eq(1);
        let learnButton = children.eq(2);
        let deleteLanguageButton = children.eq(3);

        // TODO: Add other button onclicks
        managePhrasesButton.click(() => {
            window.location.href = "/djangolearn/manage-phrases/";
        });
        deleteLanguageButton.click(() => {
            const requestUrl = `/djangolearn/api/languages/${languageName}/`;
            const csrftoken = getCookie("csrftoken");
            const init = {
                method: "DELETE",
                mode: "same-origin",
                headers : {
                    "X-CSRFToken": csrftoken
                }
            }
            fetch(requestUrl, init).then((response) => {
                return response.json();
            }).then((data) => {
                let html = null;
                let class_ = null;
                if(data.error) {
                    html = data.error;
                    class_ = "message-error";
                }
                else if(data.success) {
                    html = data.success;
                    class_ = "message-info";
                    console.log(index);
                    const languagesList = $(".languages-list");
                    languagesList.remove("li:first-child");
                    let children = languagesList.children();
                    //languagesList.remove("li:first-child");
                    languagesList.empty();
                    languagesList.append(children);
                }

                $(".messages-container").append(createMessageParagraph(html, class_));
            })
        });
    });

}
$(document).ready(() => {
    const removingTimeout = 1000;
    //$(".navigation").addClass("navigation-hidden");

   setTimeout(removeMessages, removingTimeout);
   addNavigationRollingButtonOnclick();
   addSearchButtonOnclick();
   addAddButtonOnclick();
   addDeleteLanguageButtonOnclicks();
});

