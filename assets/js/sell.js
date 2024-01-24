
let company_name = document.querySelector("#company_name");
let shares = document.querySelector("#shares");
let listNames = document.querySelector("#displayNames");
let submitButton = document.querySelector("#submitButton");
let sellForm = document.querySelector("#sellForm");
let showSellResponse = document.querySelector("#displaySellResponse");
let loading_sign = document.querySelector("#loadingSign");
let noSharesError = document.querySelector("#noSharesError");
const createElement = (element) => document.createElement(element);
let companyNames;
let companyShares;

async function getNames() {
    let url = "/api/user/company_shares";
    let sharesResponse = await fetch(url);
    companyShares = await sharesResponse.json();
    companyNames = Object.keys(companyShares);

    if (companyNames.length > 0) {
        enableForm();
    } else {
        loading_sign.classList.add("hidden");
        noSharesError.textContent = "You have no shares to sell";
        noSharesError.classList.remove("hidden");
    }
}
getNames();

function enableForm() {
    company_name.disabled = false;
    submitButton.disabled = false;
    loading_sign.classList.add("hidden");
    }

function enableShares() {
    shares.disabled = false;
    shares.setAttribute("max", companyShares[`${company_name.value}`]);
}

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
                enableShares();
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
    companyNames.forEach(name => {
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

company_name.addEventListener('focusin', () => {
    if (company_name.value === "") {
        displayOwned();
    }
});

function displayOwned() {
    while (listNames.firstChild) {
        listNames.removeChild(listNames.firstChild);
    }
    let length = companyNames.length > 5 ? 5 : companyNames.length;
    for (let i = 0; i < length; i++) {
        let name = createElement("button");
        name.classList.add("w-full", "text-left", "text-slate-500", "hover:bg-slate-400", "hover:text-white", "p-2", "rounded-lg", "focus:outline-none");
        name.textContent = companyNames[i];
        name.addEventListener('click', () => {
            company_name.value = companyNames[i];
            while (listNames.firstChild) {
                listNames.removeChild(listNames.firstChild);
                enableShares();
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

company_name.addEventListener('keyup', (event) => {
    if (event.key === "Backspace" || event.key === "Delete") {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }
    }
    if (companyNames) {
        checkNames();
    }
});

async function getSellResponse() {
    let url = `/api/sell?company_name=${company_name.value}&shares=${shares.value}`;
    response = await fetch(url);
    let sellResponse = await response.json();

    if (sellResponse.flag === "error") {
        // failed to fetch Sell
    } else if (sellResponse.flag === "success") {
        // successfully fetched Sell
        displaySell(sellResponse);
    }
    }

function displaySell(sellResponse) {
    let SellDiv = createElement("div");
    let fullMessage = createElement("div");
    let doneImage = createElement("img");
    let message = createElement("p");
    let moreMessage = createElement("p");
    let muchMessage = createElement("p");
    let companyName = createElement("p");
    let sharesSold = createElement("p");
    let price = createElement("p");
    let dismissButton = createElement("button");

    companyName.classList.add("font-bold", "text-purple-400", "block");
    sharesSold.classList.add("font-bold", "text-purple-400", "inline");
    price.classList.add("font-bold", "text-purple-400", "inline");
    message.classList.add("inline");
    moreMessage.classList.add("inline");
    muchMessage.classList.add("inline");
    SellDiv.classList.add("p-10","rounded-lg", "flex", "flex-col", "items-center", "gap-10", "shadow-sm", "shadow-slate-800", "h-1/2", "w-2/3", "bg-white");
    dismissButton.classList.add("bg-purple-800", "font-bold", "text-xl", "text-white", "p-2", "px-16", "rounded-xl", "sm:text-2xl", "sm:p-3", "sm:px-24");
    sellForm.classList.add("hidden");

    companyName.textContent = company_name.value;
    sharesSold.textContent = `${shares.value} `;
    price.textContent = `$${sellResponse.total_share_cost.toFixed(2)}`;
    message.textContent = "You have successfully sold ";
    moreMessage.textContent = ` ${shares.value === 1 ? "share" : "shares"} of `;
    muchMessage.textContent = " at ";
    doneImage.setAttribute("src", "../assets/icons/done.svg");
    dismissButton.textContent = "Ok";

    dismissButton.addEventListener('click', () => {
        sellForm.classList.remove("hidden");
        while (showSellResponse.firstChild) {
            showSellResponse.removeChild(showSellResponse.firstChild);
        }
        showSellResponse.classList.add("hidden");
        company_name.value = "";
        shares.value = "";
    });
    while (showSellResponse.firstChild) {
        showSellResponse.removeChild(showSellResponse.firstChild);
    }

    fullMessage.appendChild(message);
    fullMessage.appendChild(sharesSold);
    fullMessage.appendChild(moreMessage);
    fullMessage.appendChild(companyName);
    fullMessage.appendChild(muchMessage);
    fullMessage.appendChild(price);
    SellDiv.appendChild(doneImage);
    SellDiv.appendChild(fullMessage);
    SellDiv.appendChild(dismissButton);
    showSellResponse.appendChild(SellDiv);
}

submitButton.addEventListener('click', () => {
    let validName = false;
    companyNames.forEach(name => {
        if (name === company_name.value) {
            validName = true;
            return;
        }
    })
    if (validName && shares.value <= companyShares[`${company_name.value}`]) {
        loading();
        getSellResponse();
    } else {
        while (listNames.firstChild) {
            listNames.removeChild(listNames.firstChild);
        }
        let errorMessage = createElement("p");
        shares.value > companyShares[`${company_name.value}`] ? errorMessage.textContent = `Your maximum shares is ${companyShares[`${company_name.value}`]}` : errorMessage.textContent = "Please enter a valid company name";
        errorMessage.classList.add("text-red-500");
        listNames.appendChild(errorMessage);
    }


});

function loading () {
    // load while waiting for response
    let loadingSign = createElement("span");
    loadingSign.classList.add("loading", "loading-ring", "loading-lg");
    showSellResponse.classList.remove("hidden");
    showSellResponse.appendChild(loadingSign);
}