const navbar = document.querySelector(".header_container");
const menu = document.querySelector(".three_lin");

menu.addEventListener('click', (e) => {
    navbar.classList.toggle("active");
    e.stopPropagation();
    
});

window.addEventListener('click', (e) => {
    if (!navbar.contains(e.target) && e.target !== menu) {
        if (navbar.classList.contains("active")) {
            navbar.classList.remove("active");
        }
    }
});

function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}