/// FOR CSS

///MOBILE MENU BTN

const menubtn = document.querySelector(".menu-btn")
const navLinks = document.querySelector(".nav-links")

menubtn.addEventListener('click',()=>{
navLinks.classList.toggle('mobile-menu')
})

///CHANGE MONEY DISPLAY

var timeRanges = ["THIS WEEK", "THIS MONTH", "THIS YEAR"];
var rangeIndex = 0;
var rangeSpan = document.querySelector(".time-range span");

document.querySelector(".time-range i:first-child").addEventListener("click", function() {
    rangeIndex = (rangeIndex > 0) ? rangeIndex - 1 : timeRanges.length - 1;
    rangeSpan.innerText = timeRanges[rangeIndex];
});

document.querySelector(".time-range i:last-child").addEventListener("click", function() {
    rangeIndex = (rangeIndex < timeRanges.length - 1) ? rangeIndex + 1 : 0;
    rangeSpan.innerText = timeRanges[rangeIndex];
});