'use strict';


// function showResultPlans(evt) {
//     evt.preventDefault();
//     fetch('/plan-study-visits')
//         .then(response => response.json())
//         .then(response => {
//         document.querySelector('#visit-section').innerHTML = response;
//         });
//   }
  
// document.querySelector('#submit_visits').addEventListener('click', showResultPlans);

// add event listener to create elements on page for the new forms
// the test details form will have to be refactored into JS

function addTest(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    console.log(this)
    const cln = document.getElementsByClassName("result")[0].cloneNode(true);
    document.querySelector("#result-details").insertBefore(cln,this);
    console.log('hello world')
    return false;
}

document.querySelector("#add-test").addEventListener('click', addTest); 

