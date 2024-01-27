let navbar = document.querySelector('#navbar');
let logo = document.querySelector('#logo');
let quote = document.querySelector('#quote');
let sell = document.querySelector('#sell');
let buy = document.querySelector('#buy');
let history = document.querySelector('#history');
let profile = document.querySelector('#profile');
let hamburger = document.querySelector('#hamburger');
let hamburgerMenu = document.querySelector('#hamburgerMenu');
let hamburgerImage = document.querySelector('#hamburgerImage');
let closeButton = document.createElement('button');
let names;

async function getNames() {
    let url = 'api/company_names'
    response = await fetch(url);
    names = await response.json();
}
getNames();

closeButton.textContent = 'Close';
closeButton.setAttribute('id', 'closeButton');
closeButton.setAttribute('type', 'button');
closeButton.classList.add('text-white', 'p-1', 'hover:bg-red-400', 'rounded-lg', 'shadow-lg');

closeButton.addEventListener('click', () => {
    while (hamburgerMenu.firstChild) {
        hamburgerMenu.removeChild(hamburgerMenu.firstChild);
    }

    
    quote.classList.add('hidden');
    sell.classList.add('hidden');
    buy.classList.add('hidden');
    history.classList.add('hidden');
    profile.classList.add('hidden');
    profile.classList.remove('flex', 'flex-col');
    hamburgerMenu.classList.remove('absolute', 'top-0', 'bg-black', 'rounded-lg', 'shadow-lg', 'w-48', 'z-10');
    hamburgerMenu.appendChild(hamburgerImage);
    restoreNav();
});

function showMenu () {
    while (hamburgerMenu.firstChild) {
        hamburgerMenu.removeChild(hamburgerMenu.firstChild);
    }

    quote.classList.remove('hidden');
    sell.classList.remove('hidden');
    buy.classList.remove('hidden');
    history.classList.remove('hidden');
    profile.classList.remove('hidden');
    profile.classList.add('flex', 'flex-col');
    hamburgerMenu.classList.add('absolute', 'top-0', 'bg-black', 'rounded-lg', 'shadow-lg', 'w-48', 'z-10');

    hamburgerMenu.appendChild(quote);
    hamburgerMenu.appendChild(sell);
    hamburgerMenu.appendChild(buy);
    hamburgerMenu.appendChild(history);
    hamburgerMenu.appendChild(profile);
    hamburgerMenu.appendChild(closeButton);
}

function restoreNav () {
    while (navbar.firstChild) {
        navbar.removeChild(navbar.firstChild);
    }
    navbar.appendChild(logo);
    navbar.appendChild(quote);
    navbar.appendChild(sell);
    navbar.appendChild(buy);
    navbar.appendChild(history);
    navbar.appendChild(profile);
    navbar.appendChild(hamburger);
}