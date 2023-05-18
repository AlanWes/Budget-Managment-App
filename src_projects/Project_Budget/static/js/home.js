/// FOR CSS

///MOBILE MENU BTN

const menubtn = document.querySelector(".menu-btn")
const navLinks = document.querySelector(".nav-links")
const menubtn2 = document.querySelector(".menu-btn-after")
const body = document.body;

menubtn.addEventListener('click',()=>{
  body.style.overflow = 'hidden';
  menubtn.style.display = "none";
  menubtn2.style.display = "block";
  navLinks.classList.toggle('mobile-menu')
  navLinks.classList.remove('mobile-menu2');
})

menubtn2.addEventListener('click',()=>{
  body.style.overflow = 'auto';
  menubtn.style.display = "block";
  menubtn2.style.display = "none";
  navLinks.classList.toggle('mobile-menu2')
  navLinks.classList.remove('mobile-menu');
})

///CHANGE MONEY DISPLAY

const timeRanges = document.querySelectorAll('.time-range');

timeRanges.forEach(function(timeRange) {
  const leftArrow = timeRange.querySelector('.fa-chevron-left');
  const rightArrow = timeRange.querySelector('.fa-chevron-right');
  const option = timeRange.querySelector('span');

  const options = ['THIS WEEK', 'THIS MONTH', 'THIS YEAR'];

  let currentIndex = options.indexOf(option.textContent);

  // < left
  leftArrow.addEventListener('click', function() {
    currentIndex--;
    if (currentIndex < 0) {
      currentIndex = options.length - 1;
    }
    option.textContent = options[currentIndex];
  });

  // > right
  rightArrow.addEventListener('click', function() {
    currentIndex++;
    if (currentIndex >= options.length) {
      currentIndex = 0;
    }
    option.textContent = options[currentIndex];
  });
});




