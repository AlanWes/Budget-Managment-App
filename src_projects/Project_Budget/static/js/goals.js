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

///NAVIGATOR

const createBtn = document.querySelector('.create button');
const listBtn = document.querySelector('.list button');
const finishedBtn = document.querySelector('.finished button');
const createDiv = document.querySelector('.goals-create');
const listDiv = document.querySelector('.goals-list');
const finishedDiv = document.querySelector('.goals-finished');
const mainDiv = document.querySelector('.main');

const backBtn1 = document.querySelector('.back-btn1')
const backBtn2 = document.querySelector('.back-btn2')
const backBtn3 = document.querySelector('.back-btn3')

listDiv.style.display = "none";
finishedDiv.style.display = "none";
createDiv.style.display = "none";

createBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  createDiv.style.display = '';
});

listBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  listDiv.style.display = '';
});

finishedBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  finishedDiv.style.display = '';
});

backBtn1.addEventListener('click', () => {
  listDiv.style.display = "none";
  finishedDiv.style.display = "none";
  createDiv.style.display = "none";
  mainDiv.style.display = '';
});

backBtn2.addEventListener('click', () => {
  listDiv.style.display = "none";
  finishedDiv.style.display = "none";
  createDiv.style.display = "none";
  mainDiv.style.display = '';
});

backBtn3.addEventListener('click', () => {
  listDiv.style.display = "none";
  finishedDiv.style.display = "none";
  createDiv.style.display = "none";
  mainDiv.style.display = '';
});
