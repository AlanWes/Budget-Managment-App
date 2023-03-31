/// FOR CSS

///MOBILE MENU BTN

const menubtn = document.querySelector(".menu-btn")
const navLinks = document.querySelector(".nav-links")

menubtn.addEventListener('click',()=>{
navLinks.classList.toggle('mobile-menu')
})

///SCROLL EFFECT

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 0) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});
