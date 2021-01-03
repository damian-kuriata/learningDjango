import {getCookie, escapeHTML} from "./modules/utils.js";

// TODO: Add translations
function getPhraseFromServer(url) {
    let csrftoken = getCookie("csrftoken");
    const init = {
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken
        },
        mode: "same-origin"
    }
    return Promise.resolve(fetch(url, init).then((response) => {
        if(!response.ok) {
            throw new Error("Response issue " + response.status);
        }
        else {
            return response.json();
        }
    }).then((data) => {
        // Convert JSON string to Javascript object
        data = JSON.parse(data);
        return {
            non_translated_text: data[0].fields.non_translated_text,
            translated_text: data[0].fields.translated_text
        };
    }).catch((e) => {
        alert(gettext("Something went wrong: ") + e.message);
        return undefined;
    }));
}

/*async function checkPhraseWithServer(phrase) {
    // TODO: Implement actual checking
    return {
        state: "correct"
    }
}*/

$(document).ready(() => {

    const originalTextContainer = $(".original-text-container");
    const translatedTextInput = $("#translated-text-input");
    const nextButton = $("#next-button");
    const phraseUrl = "/djangolearn/api/learning-language/en/";

    nextButton.click(() => {
        let inputPhrase = translatedTextInput.val();
        if(!inputPhrase || inputPhrase === '') {
            alert(gettext("At first type something!"));
        }
        else {
            console.log("else");
            let phraseState = checkPhraseWithServer(inputPhrase);
            console.log(phraseState);
            if(phraseState.state === "correct") {
                console.log("corr");
                translatedTextInput.style.backgroundColor =
                    translatedTextInput.css("border-color");

                alert("test");
            }
        }
    });
    getPhraseFromServer(phraseUrl).then((phrase) => {
        if(phrase === undefined) {
            originalTextContainer.text(
                gettext("Something went wrong, refresh the page"));
        }
        else {
            originalTextContainer.text(phrase.non_translated_text);
            translatedTextInput.text(phrase.translated_text);
        }
    });

})