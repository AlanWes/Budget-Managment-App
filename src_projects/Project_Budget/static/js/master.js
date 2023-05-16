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

///SCROLL EFFECT

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 0) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});
