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

const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

const registerPassword = document.getElementById('register-password');
const passwordHelp = document.getElementById('password-help');

registerPassword.addEventListener('input', function() {
    const password = registerPassword.value;
    const strength = checkPasswordStrength(password);
    const strengthText = getStrengthText(strength);
    const strengthClass = getStrengthClass(strength);

    passwordHelp.textContent = strengthText;
    passwordHelp.className = `form-text ${strengthClass}`;
});

function checkPasswordStrength(password) {
    const passwordRegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$/;

    if (password.length < 8) {
        registerButton.disabled = true;
        return 'Weak';
    } else if (!passwordRegExp.test(password)) {
        registerButton.disabled = true;
        return 'Medium';
    } else {
        registerButton.disabled = false;
        return 'Strong';
    }
}  

function getStrengthText(strength) {
    if (strength === 'Weak') {
        return 'Weak password.\nMust be at least 12 characters long and contain 1 digit, 1 uppercase, 1 lowercase, and 1 special character [@$!%*#?&]';
    } else if (strength === 'Medium') {
        return 'Medium password.\nMust be at least 12 characters long and contain 1 digit, 1 uppercase, 1 lowercase, and 1 special character [@$!%*#?&]';
    } else {
        return 'Strong password. Good job! :)';
}
}
  
function getStrengthClass(strength) {
    if (strength === 'Weak') {
        return 'text-danger';
    } else if (strength === 'Medium') {
        return 'text-warning';
    } else {
        return 'text-success';
    }
}