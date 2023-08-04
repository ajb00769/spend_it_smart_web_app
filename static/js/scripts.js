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

const usernameRegField = document.getElementById('uname-reg');
const emailRegField = document.getElementById('email-reg');
const registerPassword = document.getElementById('register-password');
const registerPasswordConfirm = document.getElementById('register-password-confirm');
const passwordHelp = document.getElementById('password-help');

const allRegisterFormFields = document.querySelectorAll('.register-form-field');

registerPassword.addEventListener('input', function() {
    const password = registerPassword.value;
    const strength = checkPasswordStrength(password);
    const strengthText = getStrengthText(strength);
    const strengthClass = getStrengthClass(strength);

    passwordHelp.textContent = strengthText;
    passwordHelp.className = `form-text ${strengthClass}`;
});

registerPasswordConfirm.addEventListener('input', function() {
    let password = registerPassword.value;
    let passwordConfirmation = registerPasswordConfirm.value;
    let passwordConfirmText = document.getElementById('password-confirm-help');

    if (password === passwordConfirmation && checkPasswordStrength(password === 'Strong')) {
        registerButton.disabled = false;
        registerButton.hidden = false;
        passwordConfirmText.textContent = 'Passwords match. Good job! :)';
        passwordConfirmText.className = 'form-text text-success';
    } else {
        registerButton.disabled = true;
        registerButton.hidden = true;
        passwordConfirmText.textContent = 'Passwords do not match.';
        passwordConfirmText.className = 'form-text text-danger';
    }
})

function checkPasswordStrength(password) {
    const passwordRegExpUpper = /^(?=.*[A-Z])/;
    const passwordRegExpLower = /^(?=.*[a-z])/;
    const passwordRegExpDigit = /^(?=.*\d)/;
    const passwordRegExpSpecial = /^(?=.*[@$!%*#?&])/;

    if (!passwordRegExpLower.test(password)) {
        return 'No Lower';
    } else if (!passwordRegExpUpper.test(password)) {
        return 'No Upper';
    } else if (!passwordRegExpDigit.test(password)) {
        return 'No Digit';
    } else if (!passwordRegExpSpecial.test(password)) {
        return 'No Special';
    } else if (password.length < 12) {
        return 'Less than 12 characters';
    } else {
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

loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const emailLoginField = document.getElementById("login-email");
    const passwordLoginField = document.getElementById("login-password");
    const csrfToken = document.getElementById("csrf-token");
    let email = emailLoginField.value;
    let password = passwordLoginField.value;
    let csrf = csrfToken.value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf
        },
        body: JSON.stringify({ 'email': email, 'password': password })
    }).then((response) => {
        console.log(response);
        if (response.ok) {
            window.location.href = "/dashboard";
        } else {
            return response.json();
        }
    }).then((data) => {
        const errorMessage = document.getElementById("login-error-message");
        errorMessage.textContent = data.message;
    }).catch((error) => {
        console.error("Error:", error);
    })
})