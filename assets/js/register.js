
const username = document.querySelector("#username");
const password = document.querySelector("#password");
const confirm_password = document.querySelector("#confirm_password");
const submitButton = document.querySelector("#submitButton");
const displayError = document.querySelector("#displayError");
let displayUserNameError = document.querySelector("#displayUserNameError");
let displayConfirmError = document.querySelector("#displayConfirmError");
let passwordEyeImage = document.querySelector("#passwordEyeImage");
let confirmEyeImage = document.querySelector("#confirmEyeImage");
const usernamePattern = /^[a-zA-Z][a-z_A-Z0-9]{3,}$/;
const passwordPattern = /^\S{6,}$/;

async function getUser() {
    let url = `/api/register?username=${username.value}`;
    let response = await fetch(url);
    let result = await response.json();
}

username.addEventListener("keyup", () => {
    if (/\s+/.test(username.value)) {
        displayUserNameError.textContent = 'Username cannot contain spaces';
        displayUserNameError.classList.remove("hidden");
    } else if (/^[0-9]+/.test(username.value)) {
        displayUserNameError.textContent = 'Username should start with a letter';
        displayUserNameError.classList.remove("hidden");
    } else if (!/^\S{4,}$/) {
        displayUserNameError.textContent = 'Username should be at least 4 characters long';
        displayUserNameError.classList.remove("hidden");
    } else if (/^\S{4,}$/) {
        displayUserNameError.textContent = '';
        displayUserNameError.classList.add("hidden");
        getUser();
    } else {
        displayUserNameError.textContent = '';
        displayUserNameError.classList.add("hidden");
    }
});

async function register() {
    let url = `/api/register?username=${username.value}&password=${password.value}`;
    let response = await fetch(url);
    let result = await response.json();
    if (result.flag === "error") {
        displayUserNameError.textContent = 'Username already exists';
        displayUserNameError.classList.remove("hidden");
    } else if (result.flag === "success") {
        window.location.href = "/";
    }
}

function toggleVisibility (input) {
    let inputToggle = input === "password" ? password : confirm_password;
    let eyeImage = input === "password" ? passwordEyeImage : confirmEyeImage;
    if (inputToggle.type === "password") {
        inputToggle.type = "text";
        eyeImage.src = "../assets/icons/eye_closed.svg";
    } else {
        inputToggle.type = "password";
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
    } else if (password.value !== confirm_password.value) {
        displayError.textContent = 'Passwords do not match';
        displayError.classList.remove("hidden");
    } else if (!passwordPattern.test(password.value)) {
        displayError.textContent = 'Password should be at least 6 characters long';
        displayError.classList.remove("hidden");
    } else {
        register();
    }
}

submitButton.addEventListener("click", () => {
    displayError.classList.add("hidden");
    validateForm();
});