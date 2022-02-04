'use strict';

// displays a follow up question about when a result will be returned if user clicks yes to returning it
function displayTimingQuestion(evt) {
    const test = evt.target.classList[0];
    const value = evt.target.value;
  
    // displays question
    if (value === 'yes') {
        document.querySelector(`#return-timing.${test}`).style.display = '';
    }
    // hides question if user changes their selection for previous return question to "no"
    else if (value === 'no') {
        document.querySelector(`#return-timing.${test}`).style.display = 'none';
    }
}

// add event listener to each return question for each test on page
document.querySelectorAll('.return_plan').forEach( element => {
    element.addEventListener('click', displayTimingQuestion);
})

// hides each question when page is initially loaded
document.querySelectorAll('.return-timing').forEach( element => element.style.display = 'none');

    