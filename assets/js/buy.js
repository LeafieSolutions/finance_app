
let company_name = document.querySelector("#company_name");
let listNames = document.querySelector("#displayNames");
let submitButton = document.querySelector("#submitButton");
let displayError = document.querySelector("#displayError");
let displaySharesError = document.querySelector("#displaySharesError");
let shares = document.querySelector("#shares");
let buyForm = document.querySelector("#buyForm");
let showBuyResponse = document.querySelector("#displayBuyResponse");
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

submitButton.addEventListener('click', () => {
    let validName = false;
    let validShares = false;
    names.forEach(name => {
        if (name === company_name.value) {
            validName = true;
            return;
        }
    });
    if (!validName) {
        displayError.classList.remove("hidden");
        return;
    } else {
        displayError.classList.add("hidden");
    }
    if (shares.value < 1) {
            displaySharesError.classList.remove("hidden");
    } else {
        displaySharesError.classList.add("hidden");
        validShares = true;
    }
    if (validName && validShares) {
        loading();
        getBuyResponse();
    } else {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }
    }
});

function loading () {
    let loadingSign = createElement('p');
    loadingSign.classList.add("loading", "loading-ring", "loading-lg");
    showBuyResponse.classList.remove("hidden");
    showBuyResponse.appendChild(loadingSign);
}

async function getBuyResponse() {
    let url = `/api/buy?company_name=${company_name.value}&shares=${shares.value}`;
    response = await fetch(url);
    let buyResponse = await response.json();

    if (buyResponse.flag === "error") {
        // failed to fetch Buy
        if (buyResponse.reason === "insufficient cash") {
            displayBuy(buyResponse);
        }
    } else if (buyResponse.flag === "success") {
        // successfully fetched Buy
        displayBuy(buyResponse);
    }
}

function displayBuy (buyResponse) {
    let buyDiv = createElement("div");
    let fullMessage = createElement("div");
    let doneImage = createElement("img");
    let message = createElement("p");
    let moreMessage = createElement("p");
    let muchMessage = createElement("p");
    let companyName = createElement("p");
    let sharesValue = createElement("p");
    let remainingCash = createElement("p");
    let dismissButton = createElement("button");

    companyName.classList.add("font-bold", "text-purple-400", "inline");
    sharesValue.classList.add("font-bold", "text-purple-400", "inline");
    remainingCash.classList.add("font-bold", "text-purple-400", "inline");
    message.classList.add("inline");
    moreMessage.classList.add("inline");
    muchMessage.classList.add("inline");
    showBuyResponse.classList.remove("hidden");
    buyDiv.classList.add("p-10","rounded-lg", "flex", "flex-col", "items-center", "gap-10", "shadow-sm", "shadow-slate-800", "h-1/2", "w-2/3", "bg-white");
    dismissButton.classList.add("bg-purple-800", "font-bold", "text-xl", "text-white", "p-2", "px-16", "rounded-xl", "sm:text-2xl", "sm:p-3", "sm:px-24");
    buyForm.classList.add("hidden");

    try {
        if (buyResponse.reason === "insufficient cash") {
            message.textContent = "You don't have enough cash to buy ";
            moreMessage.textContent = ` ${shares.value === 1 ? "share" : "shares"} of `;
            sharesValue.textContent = shares.value;
            companyName.textContent = company_name.value;
            remainingCash.textContent = ` $${buyResponse.cash.toFixed(2)} `;
            muchMessage.textContent = ` Your balance is `;
            dismissButton.textContent = "Ok";

            dismissButton.addEventListener('click', () => {
                showBuyResponse.classList.add("hidden");
                buyForm.classList.remove("hidden");
                showBuyResponse.removeChild(showBuyResponse.firstChild);
                company_name.value = "";
                shares.value = "";
            });

            while (showBuyResponse.firstChild) {
                showBuyResponse.removeChild(showBuyResponse.firstChild);
            }

            fullMessage.appendChild(message);
            fullMessage.appendChild(sharesValue);
            fullMessage.appendChild(moreMessage);
            fullMessage.appendChild(companyName);
            fullMessage.appendChild(muchMessage);
            fullMessage.appendChild(remainingCash);
            buyDiv.appendChild(fullMessage);
            buyDiv.appendChild(dismissButton);
            showBuyResponse.appendChild(buyDiv);
            return;
        }
    } catch (error) {
        // ignore error
    }

    while (showBuyResponse.firstChild) {
        showBuyResponse.removeChild(showBuyResponse.firstChild);
    }

    companyName.textContent = company_name.value;
    sharesValue.textContent = buyResponse.shares;
    message.textContent = "You've successfully bought ";
    moreMessage.textContent = ` ${buyResponse.shares === 1 ? "share" : "shares"} of `;
    doneImage.setAttribute("src", "../assets/icons/done.svg");
    dismissButton.textContent = "Ok";

    dismissButton.addEventListener('click', () => {
        showBuyResponse.classList.add("hidden");
        buyForm.classList.remove("hidden");
        showBuyResponse.removeChild(showBuyResponse.firstChild);
        company_name.value = "";
        shares.value = "";
    });

    while (showBuyResponse.firstChild) {
        showBuyResponse.removeChild(showBuyResponse.firstChild);
    }

    fullMessage.appendChild(message);
    fullMessage.appendChild(sharesValue);
    fullMessage.appendChild(moreMessage);
    fullMessage.appendChild(companyName);
    buyDiv.appendChild(doneImage);
    buyDiv.appendChild(fullMessage);
    buyDiv.appendChild(dismissButton);
    showBuyResponse.appendChild(buyDiv);
}