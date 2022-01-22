'use strict';

function checkParticipantId(evt) {
    evt.preventDefault();

    const participantId = document.querySelector('#participant_id').value;
    fetch(`/check-participant.json/${participantId}`)
    .then(response => response.json())
    .then(responseData => {
        document.querySelector('#id_check_msg').innerHTML = responseData.msg;
        console.log(responseData)
        if (responseData.code === 1) {
            document.querySelector('#study_selection').style.display = "";
        }
        else if (responseData.code === 0) {
            document.querySelector('#study_selection').style.display = "none";
        }
    })

}
document.querySelector('#study_selection').style.display = "none";
document.querySelector("#participant_id_check").addEventListener('click', checkParticipantId);