const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".login-link");
const regsiterLink = document.querySelector(".register-link");

regsiterLink.addEventListener("click", () => {
    wrapper.classList.add("active");
});

loginLink.addEventListener("click", () => {
    wrapper.classList.remove("active");
});

const loginButton = document.getElementById("loginbutton");

loginButton.addEventListener("submit", () => {
    loginButton.disabled = true;
    setTimeout(() => {
        loginButton.disabled = false;
    }, 3000);
});

const registerButton = document.getElementById("registerbutton");

registerButton.addEventListener("submit", () => {
    registerButton.disabled = true;
    setTimeout(() => {
        registerButton.disabled = false;
    }, 3000);
});
