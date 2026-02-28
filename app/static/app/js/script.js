const navbar = document.querySelector(".header_container");
const menu = document.querySelector(".three_lin");

menu.addEventListener('click', () => {
    navbar.classList.toggle("active");
    
})