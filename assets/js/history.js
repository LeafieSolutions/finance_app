
let showHistory = document.querySelector("#displayHistory");
let homeButton = document.querySelector("#homeButton");
let createElement = (element) => document.createElement(element);

function addText (text) {
    if (text === "add") {
        homeButton.classList.remove("hidden");
    } else {
        homeButton.classList.add("hidden");
    }
};

async function getHistory () {
    let url = `/api/user/history`;
    let response = await fetch(url);
    let history = await response.json();
    displayHistory(history);
}
getHistory();

function displayHistory (history) {
    for (let i = 0; i < history.length; i++) {
        let row = createElement("tr");
        let timestamp = createElement("td");
        let name = createElement("td");
        let ticker = createElement("td");
        let price = createElement("td");
        let shares = createElement("td");
        let total = createElement("td");

        price.classList.add("text-end");
        shares.classList.add("text-center");
        total.classList.add("text-end");
        timestamp.classList.add("text-start");
        i % 2 ? row.classList.add('bg-gray-300') : row.classList.add('bg-none');

        timestamp.textContent = history[i].timestamp;
        name.textContent = history[i].name;
        ticker.textContent = history[i].ticker;
        price.textContent = `$${history[i].price.toFixed(2)}`;
        shares.textContent = history[i].shares;
        total.textContent = `$${history[i].total.toFixed(2)}`;

        row.appendChild(timestamp);
        row.appendChild(name);
        row.appendChild(ticker);
        row.appendChild(price);
        row.appendChild(shares);
        row.appendChild(total);
        showHistory.appendChild(row);
    }
}