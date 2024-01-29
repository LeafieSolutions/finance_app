
const username = document.querySelector("#username");
const old_password = document.querySelector("#old_password");
const new_password = document.querySelector("#new_password");
const confirm_password = document.querySelector("#confirm_password");
const updateUsernameButton = document.querySelector("#updateUsernameButton");
const updatePasswordButton = document.querySelector("#updatePasswordButton");
let displayOldError = document.querySelector("#displayOldError");
let displayNewError = document.querySelector("#displayNewError");
let displayConfirmError = document.querySelector("#displayConfirmError");
let displayUserNameError = document.querySelector("#displayUserNameError");
let displayUserNameSuccess = document.querySelector("#displayUserNameSuccess");
let passwordEyeImage = document.querySelector("#passwordEyeImage");
let confirmEyeImage = document.querySelector("#confirmEyeImage");
let oldEyeImage = document.querySelector("#oldEyeImage");
let userName;

async function getUserName () {
    url = `/api/user/profile/username`;
    const response = await fetch(url);
    userName = await response.json();
}
getUserName();

function addText (text) {
    if (text === "add") {
        homeButton.classList.remove("hidden");
    } else {
        homeButton.classList.add("hidden");
    }
};

function toggleVisibility (input) {
    let inputToggle;
    let eyeImage;
    if (input === "new_password") {
        inputToggle = new_password;
        eyeImage = passwordEyeImage;
    } else if (input === "confirm_password") {
        inputToggle = confirm_password;
        eyeImage = confirmEyeImage;
    } else if (input === "old_password") {
        inputToggle = old_password;
        eyeImage = oldEyeImage;
    }
    if (inputToggle.type === "password") {
        inputToggle.type = "text";
        eyeImage.src = "../assets/icons/eye_closed.svg";
    } else {
        inputToggle.type = "password";
        eyeImage.src = "../assets/icons/eye_open.svg";
    }
}

async function checkUsername () {
    if (username.value === userName) {
        return;
    }
    url = `/api/register/username_exists?username=${username.value}`;
    const response = await fetch(url);
    const result = await response.json();
    displayUserNameError.classList.remove("hidden");
    if (result.answer === "exist") {
        displayUserNameError.textContent = 'Username already exists';
    } else {
        displayUserNameSuccess.textContent = 'Username available';
    }
}

async function updateUsername () {
    if (username.value === userName) {
        return;
    }
    url = `/api/user/profile/change/username?new_username=${username.value}`;
    const response = await fetch(url);
    const result = await response.json();
    if (result.flag === "success") {
        // successfully updated username
        displayUserNameError.classList.add("hidden");
        displayUserNameSuccess.textContent = 'Username updated successfully';
        displayUserNameSuccess.classList.remove("hidden");
    } else {
        displayUserNameError.textContent = 'Username already exists';
        displayUserNameError.classList.remove("hidden");
    }
}

function checkFormat (sender) {
    if (username.value === "") {
        displayUserNameError.textContent = 'Username cannot be empty';
        displayUserNameError.classList.remove("hidden");
    } else if (/\s+/.test(username.value)) {
        displayUserNameError.textContent = 'Username cannot contain spaces';
        displayUserNameError.classList.remove("hidden");
    } else if (/^[0-9]+/.test(username.value)) {
        displayUserNameError.textContent = 'Username should start with a letter';
        displayUserNameError.classList.remove("hidden");
    } else if (!/^\S{4,}$/.test(username.value)) {
        displayUserNameError.textContent = 'Username should be at least 4 characters long';
        displayUserNameError.classList.remove("hidden");
    } else if (/^\S{4,}$/.test(username.value)) {
        displayUserNameError.textContent = '';
        displayUserNameError.classList.add("hidden");
        checkUsername();
        sender === 'click' ? updateUsername() : null;
    } else {
        displayUserNameError.textContent = '';
        displayUserNameError.classList.add("hidden");
    }}

username.addEventListener("keyup", () => {
    displayUserNameError.textContent = '';
    displayUserNameError.classList.add("hidden");
    displayUserNameSuccess.textContent = '';
    displayUserNameSuccess.classList.add("hidden");
    checkFormat('keyup')
});

updateUsernameButton.addEventListener("click", () => {
    displayUserNameError.textContent = '';
    displayUserNameError.classList.add("hidden");
    displayUserNameSuccess.textContent = '';
    displayUserNameSuccess.classList.add("hidden");
    checkFormat('click');
});

function checkNewPassword () {
    if (/\s/.test(new_password.value)) {
        displayNewError.textContent = 'Password cannot contain spaces';
        displayNewError.classList.remove("hidden");
    } else if (!/^\S{6,}$/.test(new_password.value)) {
        displayNewError.textContent = 'Password should be at least 6 characters long';
        displayNewError.classList.remove("hidden");
    } else if (/^\S{6,}$/.test(new_password.value)) {
        displayNewError.textContent = '';
        displayNewError.classList.add("hidden");
        return true;
    } else {
        displayNewError.textContent = '';
        displayNewError.classList.add("hidden");
    }
    return false;
}

new_password.addEventListener("keyup", () => {
    checkNewPassword();
});

function checkConfirmPassword () {
    if (new_password.value !== confirm_password.value) {
        displayConfirmError.textContent = 'Passwords do not match';
        displayConfirmError.classList.remove("hidden");
    } else {
        displayConfirmError.textContent = '';
        displayConfirmError.classList.add("hidden");
        return true;
    }
    return false;
}

confirm_password.addEventListener("keyup", () => {
    checkConfirmPassword();
});

async function updatePassword () {
    url = `/api/user/profile/change/password?old_password=${old_password.value}&new_password=${new_password.value}`;
    const response = await fetch(url);
    const result = await response.json();
    if (result.flag === "success") {
        // successfully updated password
        displayOldError.classList.add("hidden");
        displayNewError.classList.add("hidden");
        displayConfirmError.classList.add("hidden");
        displayConfirmSuccess.textContent = 'Password updated successfully';
        displayConfirmSuccess.classList.remove("hidden");
    } else {
        displayOldError.textContent = 'Incorrect password';
        displayOldError.classList.remove("hidden");
    }
}

updatePasswordButton.addEventListener("click", () => {
    displayOldError.textContent = '';
    displayOldError.classList.add("hidden");
    displayNewError.textContent = '';
    displayNewError.classList.add("hidden");
    displayConfirmError.textContent = '';
    displayConfirmError.classList.add("hidden");
    if (checkNewPassword() && checkConfirmPassword()) {
        updatePassword();
    }
});