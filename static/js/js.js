'use strict';

function addHcp(evt) {
  evt.preventDefault();

  const participantId = document.querySelector('#participant-id').innerHTML;

  const formInputs = {
  fname: document.querySelector('#fname').value,
  lname: document.querySelector('#lname').value,
  email: document.querySelector('#email').value,
  phone: document.querySelector('#phone').value,
  practice: document.querySelector('#practice').value,
  participantId: participantId
  };

  fetch('/add-hcp.json', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {'Content-Type': 'application/json',},
  })
    .then(response => response.json())
    .then(responseJson => {
      console.log(responseJson)
    document.querySelector("#hcp_form").style.display = "none";
    document.querySelector("#form-submitted").innerHTML = `Added ${responseJson.hcp_fname} ${responseJson.hcp_lname} as your healthcare provider!`
  })
};
document.querySelector('#hcp_form_button')?.addEventListener('click', addHcp)
		
	// Create a break line element
var br = document.createElement("br");

function createHcpForm(evt) {
  evt.preventDefault();
			
	// Create a form dynamically
	var form = document.createElement("form");

	// Create an input element for Full Name
	var FN = document.createElement("input");
	FN.setAttribute("type", "text");
  FN.setAttribute("id", "fname");
	FN.setAttribute("name", "fname");
	FN.setAttribute("placeholder", "Full Name");

	// Create an input element for date of birth
	var DOB = document.createElement("input");
	DOB.setAttribute("type", "text");
	DOB.setAttribute("name", "dob");
	DOB.setAttribute("placeholder", "DOB");

	// Create an input element for emailID
	var EID = document.createElement("input");
	EID.setAttribute("type", "text");
	EID.setAttribute("name", "emailID");
	EID.setAttribute("placeholder", "E-Mail ID");

	// Create an input element for password
	var PWD = document.createElement("input");
	PWD.setAttribute("type", "password");
	PWD.setAttribute("name", "password");
	PWD.setAttribute("placeholder", "Password");

	// Create an input element for retype-password
	var RPWD = document.createElement("input");
	RPWD.setAttribute("type", "password");
	RPWD.setAttribute("name", "reTypePassword");
	RPWD.setAttribute("placeholder", "ReEnter Password");

  // create a submit button
  var s = document.createElement("input");
  s.setAttribute("type", "submit");
  s.setAttribute("id", "submitTwo");
  s.setAttribute("value", "Submit");	

  // Append the full name input to the form
  form.appendChild(FN);
                 
  // Inserting a line break
  // form.appendChild(br.cloneNode());
   
  // // Append the DOB to the form
  // form.appendChild(DOB);
  // form.appendChild(br.cloneNode());
   
  // // Append the emailID to the form
  // form.appendChild(EID);
  // form.appendChild(br.cloneNode());
   
  // // Append the Password to the form
  // form.appendChild(PWD);
  // form.appendChild(br.cloneNode());

  // // Append the ReEnterPassword to the form
  // form.appendChild(RPWD);
  // form.appendChild(br.cloneNode());
   
  // Append the submit button to the form
  form.appendChild(s);

  document.getElementById("hcp_update_form").appendChild(form);
        
}
document.querySelector('#update_hcp').addEventListener('click', createHcpForm)

function addHcpNew(evt) {
  evt.preventDefault();

  const participantId = document.querySelector('#participant-id').innerHTML;

  const formInputs = {
  fname: document.querySelector('#fname').value,
  // lname: document.querySelector('#lname').value,
  // email: document.querySelector('#email').value,
  // phone: document.querySelector('#phone').value,
  // practice: document.querySelector('#practice').value,
  participantId: participantId
  };

  fetch('/add-hcp.json', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {'Content-Type': 'application/json',},
  })
    .then(response => response.json())
    .then(responseJson => {
      console.log(responseJson)
    document.querySelector("#hcp_form").style.display = "none";
    document.querySelector("#form-submitted").innerHTML = `Added ${responseJson.hcp_fname} ${responseJson.hcp_lname} as your healthcare provider!`
  })
};
document.querySelector('#submitTwo')?.addEventListener('click', addHcpNew)



