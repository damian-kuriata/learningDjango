import {getCookie, escapeHTML} from "./modules/utils.js";

// Bool that indicated whether phrase was fetched from server or not
let canFetchPhrase;
let fetchedPhrase;

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
    let csrftoken = getCookie("csrftoken");
    let dataToSend = {
        phrase_id: fetchedPhrase.id,
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
function updateOriginalTextContainer(text) {
    const originalTextContainer = $(".original-text-container");
    if(text === undefined) {
            originalTextContainer.text(
                gettext("Something went wrong, refresh the page"));
        }
        else {
            originalTextContainer.text(text);
        }
}
$(document).ready(() => {
    const translatedTextInput = $("#translated-text-input");
    const nextButton = $("#next-button");
    const phraseUrl = "/djangolearn/api/learning-language/en/";

    nextButton.click(async (event) => {
        // TODO: implement preventing of clicking button until phrase is fetched
        if(!event.detail || event.detail === 2) {
            console.log("click");
        }
        // Wait a specified amount of seconds before fetching next phrase
        setTimeout(() => {
            canFetchPhrase = true;
        }, 2000);
        if(!canFetchPhrase) {
            return;
        }
        let inputPhrase = translatedTextInput.val();
        if(!inputPhrase || inputPhrase === '') {
            alert(gettext("At first type something!"));
        }
        else {
            let phraseCorrect = await checkPhraseWithServer(inputPhrase, phraseUrl,
                "to_foreign").then(result => result);
            // Display a message to user whether translation is correct or not..
            console.log("set false");
            canFetchPhrase = false;
            getPhraseFromServer(phraseUrl).then((phrase) => {
                console.log("set true");
                fetchedPhrase = phrase;
                updateOriginalTextContainer(phrase.non_translated_text);
            });
        }
    });
    canFetchPhrase = true;
    getPhraseFromServer(phraseUrl).then((phrase) => {
        fetchedPhrase = phrase;
        updateOriginalTextContainer(phrase.non_translated_text);
    });

})