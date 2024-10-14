const btnLoginPopup = document.querySelector('.btnLogin-popup');
const wrapper = document.querySelector('.wrapper');
const closeIcons = document.querySelectorAll('.icon-close'); // Selecting all close icons
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

// Function to open login form
btnLoginPopup.addEventListener('click', () => {
    wrapper.style.display = 'flex';
    document.querySelector('.login').style.display = 'block';
    document.querySelector('.register').style.display = 'none';
});

// Function to close forms
closeIcons.forEach(icon => {
    icon.addEventListener('click', () => {
        wrapper.style.display = 'none';
    });
});

// Function to switch to register form
registerLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    document.querySelector('.login').style.display = 'none';
    document.querySelector('.register').style.display = 'block';
});

// Function to switch back to login form
loginLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    document.querySelector('.register').style.display = 'none';
    document.querySelector('.login').style.display = 'block';
});

function togglePassword() {
    var passwordInput = document.getElementById("password");
    var toggleEye = document.getElementById("toggleEye");

    // Toggle the type attribute
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleEye.name = "eye-off-outline"; // Change icon to 'eye'
    } else {
        passwordInput.type = "password";
        toggleEye.name = "eye-outline"; // Change icon to 'eye-off'
    }
}