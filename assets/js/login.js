
const username = document.querySelector("#username");
const password = document.querySelector("#password");
const submitButton = document.querySelector("#submitButton");
const displayError = document.querySelector("#displayError");
let eyeImage = document.querySelector("#eyeImage");
const usernamePattern = /^[a-zA-Z][a-z_A-Z0-9]{3,}$/;
const passwordPattern = /^\S{6,}$/;

async function login() {
    let url = `/api/login/authenticate?username=${username.value}&password=${password.value}`;
    let response = await fetch(url);
    let result = await response.json();
    if (result.flag === "error") {
        displayError.textContent = 'Invalid Username and/or password';
        displayError.classList.remove("hidden");
    } else if (result.flag === "success") {
        window.location.href = "/";
    }
}

function toggleVisibility () {
    if (password.type === "password") {
        password.type = "text";
        eyeImage.src = "../assets/icons/eye_closed.svg";
    } else {
        password.type = "password";
        eyeImage.src = "../assets/icons/eye_open.svg";
    }
}

function validateForm() {
    if (username.value === "" || password.value === "") {
        displayError.textContent = 'Username and password cannot be empty';
        displayError.classList.remove("hidden");
    } else if (!usernamePattern.test(username.value)) {
        displayError.textContent = 'Username should be at least 4 characters long and start with a letter';
        displayError.classList.remove("hidden");
    } else if (!passwordPattern.test(password.value)) {
        displayError.textContent = 'Password should be at least 6 characters long';
        displayError.classList.remove("hidden");
    } else {
        login();
    }
}

submitButton.addEventListener("click", () => {
    validateForm();
});