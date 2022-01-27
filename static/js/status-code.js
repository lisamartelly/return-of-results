'use strict';

document.querySelector('#change_study_status').addEventListener('click', () => {
    const status = document.querySelector('#study_status').value
    const formInputs = { status: status };
    const itemId = document.querySelector('#study-id').innerHTML;

    fetch(`/update-by-attr.json/study/${itemId}`, {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {'Content-Type': 'application/json',},
    })
    .then(response => response.text())
    .then(responseText => {
    document.querySelector("#db_status").innerHTML = status;
    })
    fetch(`/study-change-email/${itemId}`)
    .then(response => response.text())
    .then(responseText => {
        document.querySelector('#update-success').innerHTML = responseText
    })
})