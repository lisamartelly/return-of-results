'use strict';

// displays/previews an extra-details box when a link is clicked without rendering new page
// implemented for participant details and study details
function showItemDetails(evt) {
    evt.preventDefault();
    
    // gets ID of item and determines whether is participant or study
    const id = evt.target.id
    const detailType = evt.target.name
  
    // gets details for that item by ID, returns and renders in a detail box
    fetch(`/${detailType}-details.json/${id}`)
    .then (response => response.json())
    .then (responseJson => {
        const content = document.querySelector(".details-container");

        // participant detail display
        if (detailType === "participant") {
            content.innerHTML =
            `
            <h3>${responseJson.fname} ${responseJson.lname}</h3>
            <p>Partitipant ID: ${responseJson.id}</p>
            <p>Phone: ${responseJson.phone}</p>
            <p>Email: ${responseJson.email}</p>
            <a href="/participants/${responseJson.id}">See more details</a>
            <br>
            <h3>Studies:</h3>
            `
        for (const study of responseJson.studies) {
        content.insertAdjacentHTML("beforeend",
            `<p><b>${study.study_name}</b></p>
            <p>ID: ${study.study_id} Status: ${study.status}
            <br>
            `
        )};}

        // study detail display
        else if (detailType === "study") {
            content.innerHTML =
            `
            <h3>${responseJson.name}</h3>
            <p>Study ID: ${responseJson.id}</p>
            <p>Status: ${responseJson.status}</p>
            <p>Investigational Product: ${responseJson.product}</p>
            <p>Investigator: ${responseJson.investigator_fname} ${responseJson.investigator_lname}

            <a href="/studies/${responseJson.id}">See more details</a>
            `
        }
        content.style.display = "";
        content.scrollIntoView({behavior: 'smooth'});
    });
}
// hides details content until a link is clicked
document.querySelector('#details-content').style.display = "none";

// adds scroll to top of detials box when clicked
document.querySelectorAll(".detail-link").forEach(item => {
    item.addEventListener('click', showItemDetails)
});
