'use strict';

function displayTimingQuestion(evt) {
    const test = evt.target.classList[0];
    const value = evt.target.value;
  
    if (value === 'yes') {
        document.querySelector(`#return-timing.${test}`).style.display = '';
    }
    else if (value === 'no') {
        document.querySelector(`#return-timing.${test}`).style.display = 'none';
    }
}

document.querySelectorAll('.return_plan').forEach( element => {
    element.addEventListener('click', displayTimingQuestion);
})

document.querySelectorAll('.return-timing').forEach( element => element.style.display = 'none');

    