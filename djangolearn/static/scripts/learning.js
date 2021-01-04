import {getCookie, escapeHTML} from "./modules/utils.js";

// A phrase a user is currently working upon
let currentPhrase;

function getServerResponse(url) {
    let csrftoken = getCookie("csrftoken");
    const init = {
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken
        },
        mode: "same-origin"
    }
    return Promise.resolve(fetch(url, init));
}
// TODO: Add translations
function getPhraseFromServer(url) {
    return Promise.resolve(getServerResponse(url).then((response) => {
        if(!response.ok) {
            throw new Error("Response issue " + response.status);
        }
        else {
            return response.json();
        }
    }).then((data) => {
        // Convert JSON string to Javascript object
        data = JSON.parse(data);
        console.log("end get");
        return {
            id: data[0].pk,
            non_translated_text: data[0].fields.non_translated_text,
            translated_text: data[0].fields.translated_text
        };
    }).catch((e) => {
        alert(gettext("Something went wrong: ") + e.message);
        return undefined;
    }));
}
function checkPhraseWithServer(phrase, url, translation_direction) {
    let csrftoken = getCookie("csrftoken");;
    let dataToSend = {
        phrase_id: currentPhrase.id,
        direction: translation_direction,
        translated_phrase: phrase
    }
    const init = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(dataToSend),
        mode: "same-origin"
    }
    return fetch(url, init).then((response) => {
        if(!response.ok) {
            throw new Error("Response issue " + response.status);
        }
        else {
            return response.json();
        }
    }).then((data) => {
        return data.correct;
    })
}
$(document).ready(() => {

    const originalTextContainer = $(".original-text-container");
    const translatedTextInput = $("#translated-text-input");
    const nextButton = $("#next-button");
    const phraseUrl = "/djangolearn/api/learning-language/en/";

    nextButton.click(async () => {
        let inputPhrase = translatedTextInput.val();
        if(!inputPhrase || inputPhrase === '') {
            alert(gettext("At first type something!"));
        }
        else {
            let phraseCorrect = await checkPhraseWithServer(inputPhrase, phraseUrl,
                "to_foreign").then(result => result);
            // Display a message to user whether translation is correct or not..
            getPhraseFromServer(phraseUrl).then((phrase) => {
                if(phrase === undefined) {
                    originalTextContainer.text(
                    gettext("Something went wrong, refresh the page"));
                }
                else {
                    originalTextContainer.text(phrase.non_translated_text);
                    currentPhrase = phrase;
                }
            });
        }
    });
    // Get phrase form server for the first time
    getPhraseFromServer(phraseUrl).then((phrase) => {
        if(phrase === undefined) {
            originalTextContainer.text(
                gettext("Something went wrong, refresh the page"));
        }
        else {
            originalTextContainer.text(phrase.non_translated_text);
            currentPhrase = phrase;
        }
    });

})