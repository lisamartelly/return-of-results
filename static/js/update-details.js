'use strict';

// way to update something on the page, learned from this tutorial: https://www.youtube.com/watch?v=PqAaHf7JKls:

function makeEditable(elementId) {
  const node = document.querySelector(`#${elementId}`).firstElementChild;
  const input = document.createElement('input');
  input.type = 'text';
  input.value = node.innerHTML;
  node.parentNode.insertBefore(input, node);
  node.parentNode.removeChild(node);
}

function processEdits(elementId) {
  const input = document.querySelector(`#${elementId}`).firstElementChild;
  const span = document.createElement('span');
  span.textContent = input.value;
  input.parentNode.insertBefore(span, input);
  input.parentNode.removeChild(input);
}

document.querySelector('#update-details-button')?.addEventListener('click', (event) => {
    const button = event.target;    
    if(button.textContent === 'Update Information') {

      makeEditable('phone')
      makeEditable('email')
      makeEditable('hcp_fullname')
      makeEditable('hcp_email')
      makeEditable('hcp_phone')
      makeEditable('hcp_practice')

      button.textContent = 'Save Updates';
    } else if(button.textContent === 'Save Updates') {

      processEdits('phone')
      processEdits('email')
      processEdits('hcp_fullname')
      processEdits('hcp_email')
      processEdits('hcp_phone')
      processEdits('hcp_practice')

      const formInputs = {
        email: document.querySelector('#email').firstElementChild.textContent,
        phone: document.querySelector('#phone').firstElementChild.textContent,
        hcp_fullname: document.querySelector('#hcp_fullname').firstElementChild.textContent,
        hcp_email: document.querySelector('#hcp_email').firstElementChild.textContent,
        hcp_phone: document.querySelector('#hcp_phone').firstElementChild.textContent,
        hcp_practice: document.querySelector('#hcp_practice').firstElementChild.textContent,
        };

      const participantId = document.querySelector('#participant-id').innerHTML;

      fetch(`/update-by-attr.json/participant/${participantId}`, {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {'Content-Type': 'application/json',},
        })
      .then(response => response.text())
      .then(responseText => {
      document.querySelector("#update-success").innerHTML = responseText;

      button.textContent = 'Update Information';
    })
    }
});