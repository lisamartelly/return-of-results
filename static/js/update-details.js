'use strict';

// update attributes exactly where they're displayed, learned a lot from this tutorial: https://www.youtube.com/watch?v=PqAaHf7JKls:

// takes a attribute display and replaces it with an input box 
// with the default value being existing attrib value
function makeEditable(elementId) {
  const node = document.querySelector(`#${elementId}`).firstElementChild;
  const input = document.createElement('input');
  input.type = 'text';
  input.value = node.innerHTML;
  node.parentNode.insertBefore(input, node);
  node.parentNode.removeChild(node);
}

// saves everything in inputs as new attribute values
function processEdits(elementId) {
  const input = document.querySelector(`#${elementId}`).firstElementChild;
  const span = document.createElement('span');
  span.textContent = input.value;
  input.parentNode.insertBefore(span, input);
  input.parentNode.removeChild(input);
}

// when update button is clicked, makes certain fields editable
document.querySelector('#update-details-button')?.addEventListener('click', (event) => {
    const button = event.target;    
    if(button.textContent === 'Update Information') {

      // specifies which elements on details page to make editable
      makeEditable('phone')
      makeEditable('email')
      makeEditable('hcp_fullname')
      makeEditable('hcp_email')
      makeEditable('hcp_phone')
      makeEditable('hcp_practice')

      // changes button to save updates if it's in edit mode
      button.textContent = 'Save Updates';
      
      // if save button is clicked
    } else if(button.textContent === 'Save Updates') {

      // saves values in each input box
      processEdits('phone')
      processEdits('email')
      processEdits('hcp_fullname')
      processEdits('hcp_email')
      processEdits('hcp_phone')
      processEdits('hcp_practice')

      // packages form values to send to db
      const formInputs = {
        email: document.querySelector('#email').firstElementChild.textContent,
        phone: document.querySelector('#phone').firstElementChild.textContent,
        hcp_fullname: document.querySelector('#hcp_fullname').firstElementChild.textContent,
        hcp_email: document.querySelector('#hcp_email').firstElementChild.textContent,
        hcp_phone: document.querySelector('#hcp_phone').firstElementChild.textContent,
        hcp_practice: document.querySelector('#hcp_practice').firstElementChild.textContent,
        };

      const participantId = document.querySelector('#participant-id').innerHTML;

      // sends attrib values to server
      fetch(`/update-by-attr.json/participant/${participantId}`, {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {'Content-Type': 'application/json',},
        })
      .then(response => response.text())
      .then(responseText => {
        alert(responseText)
      // document.querySelector("#update-success").innerHTML = responseText;

      button.textContent = 'Update Information';
    })
    }
});