'use strict';

// displays/previews an extra-details box when a link is clicked without rendering new page
// implemented for participant details and study details
function showItemDetails(evt) {
    evt.preventDefault();
    
    // gets ID of item and determines whether is participant or study
    
    const id = evt.target.parentElement.id
    const detailType = evt.target.parentElement.name
  
    // gets details for that item by ID, returns and renders in a detail box
    fetch(`/${detailType}-details.json/${id}`)
    .then (response => response.json())
    .then (responseJson => {
        const content = document.querySelector("#details-content");

        // participant detail display
        if (detailType === "participant") {
            content.innerHTML =
            `
            <h3>${responseJson.fname} ${responseJson.lname}</h3>
            <p><b>Partitipant ID:</b> ${responseJson.id}</p>
            <p><b>Phone:</b> ${responseJson.phone}</p>
            <p><b>Email:</b> ${responseJson.email}</p>
            <a href="/participants/${responseJson.id}"><button class="button">See Participant Details</button></a>
            <br>
            <h3>Studies ${responseJson.fname} is enrolled in:</h3>
            `
        for (const study of responseJson.studies) {
        content.insertAdjacentHTML("beforeend",
            `<p><b>${study.study_name}</b></p>
            <p><b>ID:</b> ${study.study_id} <b>Status:</b> ${study.status}</p>
            `
        )};}

        // study detail display
        else if (detailType === "study") {
            content.innerHTML =
            `
            <h3>${responseJson.name}</h3>
            <p><b>Study ID:</b> ${responseJson.id}</p>
            <p><b>Status:</b> ${responseJson.status}</p>
            <p><b>Investigational Product:</b> ${responseJson.product}</p>
            <p><b>Investigator:</b> ${responseJson.investigator_fname} ${responseJson.investigator_lname}</p>

            <a href="/studies/${responseJson.id}"><button class="button" >See Study Details</button></a>
            <br><br>
            `
        }
        content.style.display = "";
        // scroll up to detail display incase out of view
        document.querySelector('.details-container').scrollIntoView({behavior: 'smooth'});
    });
}
// hides details content until a link is clicked
document.querySelector('#details-content').style.display = "none";

// adds scroll to top of detials box when clicked
document.querySelectorAll(".detail-link").forEach(item => {
    item.addEventListener('click', showItemDetails)
});
