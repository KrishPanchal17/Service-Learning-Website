const btnLoginPopup = document.querySelector('.btnLogin-popup');
const wrapper = document.querySelector('.wrapper');
const closeIcon = document.querySelector('.icon-close');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

btnLoginPopup.addEventListener('click', () => {
    wrapper.style.display = 'flex';
    document.querySelector('.login').style.display = 'block';
    document.querySelector('.register').style.display = 'none';
});

closeIcon.addEventListener('click', () => {
    wrapper.style.display = 'none';
});

registerLink.addEventListener('click', () => {
    document.querySelector('.login').style.display = 'none';
    document.querySelector('.register').style.display = 'block';
});

loginLink.addEventListener('click', () => {
    document.querySelector('.register').style.display = 'none';
    document.querySelector('.login').style.display = 'block';
});
