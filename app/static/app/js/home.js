const slider = document.getElementById("slider");
const image = slider.querySelectorAll("img");


let count = 0;

function showSlide(i) {
    if (i < 0) {
        count = image.length - 1;
    }
    else if (i >= image.length) {
        count = 0;
    }
    else {
        count = i;
    }



    slider.style.transform = `translateX(${-count * 100}vw)`;
}



setInterval(function () {
    showSlide(count + 1)
}, 5000)

