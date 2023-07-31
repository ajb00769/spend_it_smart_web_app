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
    const passwordRegExpUpper = /^(?=.*[A-Z])/;
    const passwordRegExpLower = /^(?=.*[a-z])/;
    const passwordRegExpDigit = /^(?=.*\d)/;
    const passwordRegExpSpecial = /^(?=.*[@$!%*#?&])/;

    if (!passwordRegExpLower.test(password)) {
        registerButton.disabled = true;
        registerButton.hidden = true;
        return 'No Lower';
    } else if (!passwordRegExpUpper.test(password)) {
        registerButton.disabled = true;
        registerButton.hidden = true;
        return 'No Upper';
    } else if (!passwordRegExpDigit.test(password)) {
        registerButton.disabled = true;
        registerButton.hidden = true;
        return 'No Digit';
    } else if (!passwordRegExpSpecial.test(password)) {
        registerButton.disabled = true;
        registerButton.hidden = true;
        return 'No Special';
    } else if (password.length < 12) {
        registerButton.disabled = true;
        registerButton.hidden = true;
        return 'Less than 12 characters';
    } else {
        registerButton.disabled = false;
        registerButton.hidden = false;
        return 'Strong';
    }
}  

function getStrengthText(strength) {
    if (strength === 'No Lower') {
        return "Password must contain a lowercase letter.";
    } else if (strength === 'No Upper') {
        return "Password must contain an uppercase letter.";
    } else if (strength === 'No Special') {
        return "Password must contain any of the following special characters: @$!%*#?&";
    } else if (strength === 'No Digit') {
        return "Password must contain a digit";
    } else if (strength === 'Less than 12 characters') {
        return "Password is less than 12 characters long.";
    } else {
        return "Strong password. Good Job! :)"
    }
}
  
function getStrengthClass(strength) {
    if (strength === 'No Upper' || strength === 'No Lower' || strength === 'No Digit' || strength === 'No Special') {
        return 'text-danger';
    } else if (strength === 'Less than 12 characters') {
        return 'text-danger';
    } else {
        return 'text-success';
    }
}