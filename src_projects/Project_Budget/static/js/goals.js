/// FOR CSS

///NAVIGATOR

const createBtn = document.querySelector('.create button');
const listBtn = document.querySelector('.list button');
const finishedBtn = document.querySelector('.finished button');
const createDiv = document.querySelector('.goals-create');
const listDiv = document.querySelector('.goals-list');
const finishedDiv = document.querySelector('.goals-finished');
const mainDiv = document.querySelector('.main');

listDiv.classList.add('hidden');
finishedDiv.classList.add('hidden');
createDiv.classList.add('hidden');

createBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  createDiv.classList.remove('hidden');
});

listBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  listDiv.classList.remove('hidden');
});

finishedBtn.addEventListener('click', () => {
  mainDiv.style.display = 'none';
  finishedDiv.classList.remove('hidden');
});
