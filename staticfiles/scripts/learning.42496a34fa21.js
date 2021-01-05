import {getCookie, escapeHTML} from "./modules/utils.js";

// Bool that indicated whether phrase was fetched from server or not
let canFetchPhrase = false;
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
function updateTextContainers(text) {
    const originalTextContainer = $(".original-text-container");
    const translatedTextInput = $("#translated-text-input");
    // Clear text in input
    translatedTextInput.val('');
    if(text === undefined) {
        originalTextContainer.text(
            gettext("Something went wrong, refresh the page")
        );
    }
    else {
        originalTextContainer.text(text);
    }
}
function onPhraseCorrect() {
    const goodjob = document.querySelector("#goodjob");
    const goodjobMsg = $("p.goodjob-msg");
    goodjobMsg.show();
    goodjob.play();
    // Hide after specified seconds
    const timeout = 1500;
    setTimeout(() => {
        goodjobMsg.hide();
    }, timeout);

}
function onPhraseIncorrect() {
    const badjob = document.querySelector("#badjob");
    const badjobMsg = $("p.badjob-msg");
    badjobMsg.show();
    badjob.play();
    // Hide after specified seconds
    const timeout = 1500;
    setTimeout(() => {

        badjobMsg.hide();
    }, timeout);
}
$(document).ready(() => {
    const translatedTextInput = $("#translated-text-input");
    const nextButton = $("#next-button");
    const phraseUrl = "/djangolearn/api/learning-language/en/";

    nextButton.click(async (event) => {
        let inputPhrase = translatedTextInput.val();
        if(!inputPhrase || inputPhrase === '') {
            alert(gettext("At first type something!"));
        }
        else {
            // Disable button until phrase is checked and next phrase is fetched
            nextButton.prop("disabled", true);
            let phraseCorrect = await checkPhraseWithServer(inputPhrase, phraseUrl,
                "to_foreign").then(result => result);
            // Display a message to user whether translation is correct or not..
            if(phraseCorrect) {
                onPhraseCorrect();
            }
            else {
                onPhraseIncorrect();
            }
            getPhraseFromServer(phraseUrl).then((phrase) => {
                canFetchPhrase = true;
                nextButton.prop("disabled", false);
                fetchedPhrase = phrase;
                updateTextContainers(phrase.non_translated_text);
            });
        }
    });
    getPhraseFromServer(phraseUrl).then((phrase) => {
        fetchedPhrase = phrase;
        updateTextContainers(phrase.non_translated_text);
    });

})