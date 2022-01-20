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

document.querySelector('#update-details-button').addEventListener('click', (event) => {
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

      fetch(`/update.json/${participantId}`, {
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



// function addHcp(evt) {
//   evt.preventDefault();

//   const participantId = document.querySelector('#participant-id').innerHTML;
//   const formInputs = {
//   hcp_fullname: document.querySelector('#fname').value,
//   hcp_email: document.querySelector('#email').value,
//   hcp_phone: document.querySelector('#phone').value,
//   hcp_practice: document.querySelector('#practice').value,
//   };

//   fetch(`/update.json/${participantId}`, {
//     method: 'POST',
//     body: JSON.stringify(formInputs),
//     headers: {'Content-Type': 'application/json',},
//   })
//     .then(response => response.text())
//     .then(responseText => {
//     document.querySelector("#hcp_form").style.display = "none";
//     document.querySelector("#form-submitted").innerHTML = responseText;
//   })
// };
// document.querySelector('#hcp_form_button')?.addEventListener('click', addHcp)
		
// // Create a break line element
// var br = document.createElement("br");
// function createHcpForm(evt) {
//   evt.preventDefault();
// 	// Create a form dynamically
// 	var form = document.createElement("form");
// 	// Create an input element for Full Name
// 	var fname = document.createElement("input");
// 	fname.setAttribute("type", "text");
//   fname.setAttribute("id", "fname");
// 	fname.setAttribute("name", "fname");
// 	fname.setAttribute("placeholder", "first name");

// 	// Create an input element for date of birth
// 	var DOB = document.createElement("input");
// 	DOB.setAttribute("type", "text");
// 	DOB.setAttribute("name", "dob");
// 	DOB.setAttribute("placeholder", "DOB");

// 	// Create an input element for emailID
// 	var EID = document.createElement("input");
// 	EID.setAttribute("type", "text");
// 	EID.setAttribute("name", "emailID");
// 	EID.setAttribute("placeholder", "E-Mail ID");

// 	// Create an input element for password
// 	var PWD = document.createElement("input");
// 	PWD.setAttribute("type", "password");
// 	PWD.setAttribute("name", "password");
// 	PWD.setAttribute("placeholder", "Password");

// 	// Create an input element for retype-password
// 	var RPWD = document.createElement("input");
// 	RPWD.setAttribute("type", "password");
// 	RPWD.setAttribute("name", "reTypePassword");
// 	RPWD.setAttribute("placeholder", "ReEnter Password");

//   // create a submit button
//   var s = document.createElement("input");
//   s.setAttribute("type", "submit");
//   s.setAttribute("id", "submitTwo");
//   s.setAttribute("value", "Submit");	

//   // Append the full name input to the form
//   form.appendChild(FN);
                 
//   // Inserting a line break
//   // form.appendChild(br.cloneNode());
   
//   // // Append the DOB to the form
//   // form.appendChild(DOB);
//   // form.appendChild(br.cloneNode());
   
//   // // Append the emailID to the form
//   // form.appendChild(EID);
//   // form.appendChild(br.cloneNode());
   
//   // // Append the Password to the form
//   // form.appendChild(PWD);
//   // form.appendChild(br.cloneNode());

//   // // Append the ReEnterPassword to the form
//   // form.appendChild(RPWD);
//   // form.appendChild(br.cloneNode());
   
//   // Append the submit button to the form
//   form.appendChild(s);
//   document.getElementById("hcp_update_form").appendChild(form);    
// }


// document.querySelector('#update_hcp')?.addEventListener('click', createHcpForm)

// function updateHcp(evt) {
//   evt.preventDefault();

//   const participantId = document.querySelector('#participant-id').innerHTML;

//   const formInputs = {
//   fname: document.querySelector('#fname').value,
//   // lname: document.querySelector('#lname').value,
//   // email: document.querySelector('#email').value,
//   // phone: document.querySelector('#phone').value,
//   // practice: document.querySelector('#practice').value,
//   participantId: participantId
//   };

//   fetch('/add-hcp.json', {
//     method: 'POST',
//     body: JSON.stringify(formInputs),
//     headers: {'Content-Type': 'application/json',},
//   })
//     .then(response => response.json())
//     .then(responseJson => {
//       console.log(responseJson)
//     document.querySelector("#hcp_form").style.display = "none";
//     document.querySelector("#form-submitted").innerHTML = `Added ${responseJson.hcp_fname} ${responseJson.hcp_lname} as your healthcare provider!`
//   })
// };
// document.querySelector('#submitTwo')?.addEventListener('click', updateHcp)



