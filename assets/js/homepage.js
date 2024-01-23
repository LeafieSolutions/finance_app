
let displayCash = document.querySelector("#displayCash");
let displayStocksTotal = document.querySelector("#displayStocksTotal");
let displayPortfolioTotal = document.querySelector("#displayPortfolioTotal");
let displayState = document.querySelector("#displayState");
let displaySharesTotal = document.querySelector("#displaySharesTotal");
let loading = document.querySelector("#loading");
let createElement = (element) => document.createElement(element);

async function getSummary () {
    let url = `/api/user/summary`;
    let response = await fetch(url);
    let summary = await response.json();
    loading.classList.add("hidden");
    displaySummary(summary);
}
getSummary();

function displaySummary (summary) {
    displayCash.textContent = `$${summary.cash.toFixed(2)}`;
    displayStocksTotal.textContent = `$${summary.stocks_total.toFixed(2)}`;
    displayPortfolioTotal.textContent = `$${summary.portfolio_total.toFixed(2)}`;
    displaySharesTotal.textContent = `$${summary.stocks_total.toFixed(2)}`;
    for (let i = 0; i < summary.state.length; i++) {
        let row = createElement("tr");
        let name = createElement("td");
        let ticker = createElement("td");
        let price = createElement("td");
        let shares = createElement("td");
        let total = createElement("td");

        price.classList.add("text-end");
        shares.classList.add("text-end");
        total.classList.add("text-end");
        i % 2 ? row.classList.add('bg-gray-300') : row.classList.add('bg-none');

        name.textContent = summary.state[i].name;
        ticker.textContent = summary.state[i].ticker;
        price.textContent = `$${summary.state[i].price.toFixed(2)}`;
        shares.textContent = summary.state[i].shares;
        total.textContent = `$${summary.state[i].total.toFixed(2)}`;
        row.appendChild(name);
        row.appendChild(ticker);
        row.appendChild(price);
        row.appendChild(shares);
        row.appendChild(total);
        displayState.appendChild(row);
    }
}