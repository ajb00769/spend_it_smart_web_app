const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".login-link");
const regsiterLink = document.querySelector(".register-link");

regsiterLink.addEventListener("click", () => {
  wrapper.classList.add("active");
});

loginLink.addEventListener("click", () => {
  wrapper.classList.remove("active");
});

const button = document.querySelector(".btn");
button.addEventListener("submit", () => {
  button.classList.add("disabled");
});
