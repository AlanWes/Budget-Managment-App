/// FOR CSS

///MOBILE MENU BTN

const menubtn = document.querySelector(".menu-btn")
const navLinks = document.querySelector(".nav-links")

menubtn.addEventListener('click',()=>{
navLinks.classList.toggle('mobile-menu')
})

///GOALS

const goalsForm = document.querySelector('.goals form');
const goalsDiv = document.querySelector('.goals');
const goalsAfterDiv = document.querySelector('.goals-after');

goalsForm.addEventListener('submit', function(event) {
  event.preventDefault();
  goalsDiv.classList.toggle('hidden');
  goalsAfterDiv.classList.toggle('hidden');
  const savingsGoalText = document.querySelector('#savings-goal-text');
  savingsGoalText.innerText = document.querySelector('#savings-goal').value;
  const debtGoalText = document.querySelector('#debt-goal-text');
  debtGoalText.innerText = document.querySelector('#debt-goal').value;
  const investmentGoalText = document.querySelector('#investment-goal-text');
  investmentGoalText.innerText = document.querySelector('#investment-goal').value;
});
