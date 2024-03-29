
let company_name = document.querySelector("#company_name");
let listNames = document.querySelector("#displayNames");
let submitButton = document.querySelector("#submitButton");
let quoteForm = document.querySelector("#quoteForm");
let showQuoteResponse = document.querySelector("#displayQuoteResponse");
const createElement = (element) => document.createElement(element);
let matched = [];

function addText (text) {
    if (text === "add") {
        homeButton.classList.remove("hidden");
    } else {
        homeButton.classList.add("hidden");
    }
};

function displayNames() {
    while (listNames.firstChild) {
        listNames.removeChild(listNames.firstChild);
    }
    let length = matched.length > 5 ? 5 : matched.length;
    for (let i = 0; i < length; i++) {
        let name = createElement("button");
        name.classList.add("w-full", "text-left", "text-slate-500", "hover:bg-slate-400", "hover:text-white", "p-2", "rounded-lg", "focus:outline-none");
        name.textContent = matched[i];
        name.addEventListener('click', () => {
            company_name.value = matched[i];
            while (listNames.firstChild) {
                listNames.removeChild(listNames.firstChild);
            }
        });
        name.addEventListener('mouseover', () => {
            name.classList.add("bg-slate-400");
        });
        name.addEventListener('mouseout', () => {
            name.classList.remove("bg-slate-400");
        });
        listNames.appendChild(name);
    }
}

function checkNames() {
    matched = [];
    let userName = company_name.value;
    if (userName.length < 1) {
        return;
    }
    let matchName = new RegExp(userName, "i");
    names.forEach(name => {
        if (matchName.test(name)) {
            matched.push(name);
        }
    });
    if (matched.length > 0) {
        displayNames();
    } else {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }

    }
}

company_name.addEventListener('keyup', (event) => {
    if (event.key === "Backspace" || event.key === "Delete") {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }
    }
    if (names) {
        checkNames();
    }
});

async function getQuoteResponse() {
    let url = `/api/quote?company_name=${company_name.value}`;
    response = await fetch(url);
    let quoteResponse = await response.json();

    if (quoteResponse.flag === "error") {
        // failed to fetch quote
    } else if (quoteResponse.flag === "success") {
        // successfully fetched quote
        displayQuote(quoteResponse);
    }
    }

function displayQuote(quoteResponse) {
    let quoteDiv = createElement("div");
    let fullMessage = createElement("div");
    let doneImage = createElement("img");
    let message = createElement("p");
    let moreMessage = createElement("p");
    let companyName = createElement("p");
    let price = createElement("p");
    let dismissButton = createElement("button");

    companyName.classList.add("font-bold", "text-purple-400", "inline");
    price.classList.add("font-bold", "text-purple-400", "block");
    message.classList.add("inline");
    moreMessage.classList.add("inline");
    quoteDiv.classList.add("p-10","rounded-lg", "flex", "flex-col", "items-center", "gap-10", "shadow-sm", "shadow-slate-800", "h-1/2", "w-2/3", "bg-white");
    dismissButton.classList.add("bg-purple-800", "font-bold", "text-xl", "text-white", "p-2", "px-16", "rounded-xl", "sm:text-2xl", "sm:p-3", "sm:px-24");
    quoteForm.classList.add("hidden");

    companyName.textContent = quoteResponse.name;
    price.textContent = `$${quoteResponse.price}`;
    message.textContent = 'A share of ';
    moreMessage.textContent = ' is ';
    doneImage.setAttribute("src", "../assets/icons/done.svg");
    dismissButton.textContent = "Ok";

    dismissButton.addEventListener('click', () => {
        showQuoteResponse.classList.add("hidden");
        quoteForm.classList.remove("hidden");
        showQuoteResponse.removeChild(showQuoteResponse.firstChild);
        company_name.value = "";
    });
    while (showQuoteResponse.firstChild) {
        showQuoteResponse.removeChild(showQuoteResponse.firstChild);
    }

    fullMessage.appendChild(message);
    fullMessage.appendChild(companyName);
    fullMessage.appendChild(moreMessage);
    fullMessage.appendChild(price);
    quoteDiv.appendChild(doneImage);
    quoteDiv.appendChild(fullMessage);
    quoteDiv.appendChild(dismissButton);
    showQuoteResponse.appendChild(quoteDiv);
}

submitButton.addEventListener('click', () => {
    let validName = false;
    names.forEach(name => {
        if (name === company_name.value) {
            validName = true;
            return;
        }
    })
    if (validName) {
        loading();
        getQuoteResponse();
    } else {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }
        let errorMessage = createElement("p");
        errorMessage.textContent = "Please enter a valid company name";
        errorMessage.classList.add("text-red-500");
        listNames.appendChild(errorMessage);
    }


});

function loading () {
    // load while waiting for response
    let loadingSign = createElement("span");
    loadingSign.classList.add("loading", "loading-ring", "loading-lg");
    showQuoteResponse.classList.remove("hidden");
    showQuoteResponse.appendChild(loadingSign);
}