
function ResultsForm() {
    // learned a lot from this: https://bapunawarsaddam.medium.com/add-and-remove-form-fields-dynamically-using-react-and-react-hooks-3b033c3c0bf5
    
    // if user arrives at page via query string, use query string values as form inputs
    React.useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        setParticipantId(urlParams.get('participantId'));
        setStudySelected(urlParams.get('studyId'));
        document.getElementById('studyId').value = urlParams.get('studyId')
        document.getElementById('participantId').value = urlParams.get('participantId')
        }, []);

    // create form input of study names in dropdown 
    const [studies, setStudies] = React.useState([]);
    React.useEffect(() =>  {
        if (participantId != null) {
        fetch('/studies.json')
        .then(response => response.json())
        .then(result => setStudies(result))
        }
    }, []);
        
    // fetch all tests and unique visits based on selected study
    const [studySelected, setStudySelected] = React.useState(null);
    const [allTests, setAllTests] = React.useState([]);
    const [allVisits, setAllVisits] = React.useState([]);

    React.useEffect(() => { 
        if (studySelected === null) { return }
        fetch(`/visits-results.json/${studySelected}`)
        .then(response => response.json())
        .then(result => {
            setAllTests(result);
            const visits = []
            for (const test of result) {
                if (visits.includes(test.visit)) { continue }
                else (visits.push(test.visit))
            };
            setAllVisits(visits);
        })   
    }, [studySelected]);

    // set study based on user input
    const handleStudySelected = evt => {
        const id = evt.target.value;
        setStudySelected(id);
    }

    // validate that participant is in study that is selected
    const [participantId, setParticipantId] = React.useState([]);

    React.useEffect(() => {
        if (participantId === null) { return }
        if (studySelected === null) { return }
        fetch(`/study-participants.json/${studySelected}/${participantId}`)
        .then(response => response.json())
        .then(responseData => {
            
            document.querySelector('#id_check_msg').innerHTML = responseData.msg;
            if (responseData.code === 1) {
                document.querySelector('#resultsInput').style.display = "";
                document.querySelector('#hcp_info').style.display = "none";
                document.querySelector('#hcp_info').innerHTML = `
                <h3>Participant's Healthcare Provider Contact Info For Urgent Results:</h3>
                <p><b>HCP Full Name:</b> ${responseData.hcp_phone} </p>
                <p><b>HCP Phone:</b> ${responseData.hcp_phone} </p>
                <p><b>HCP Email:</b> ${responseData.hcp_email} </p>
                <p><b>HCP Practice:</b> ${responseData.hcp_practice} </p>
                `
            }
            else if (responseData.code === 0) {
                document.querySelector('#resultsInput').style.display = "none";
            }
        })
    }, [participantId, studySelected]);

    // set participant ID based on user input
    const handleParticipantInput = evt => {
        const id = document.querySelector('#participantId').value;
        setParticipantId(id);
    }

    // create test input based on selected visit
    const [visitSelected, setVisitSelected] = React.useState(null);
    const [tests, setTests] = React.useState([]);

    React.useEffect(() => { 
        if (visitSelected === null) { return }
        const tests = []
        for (const visititem of allTests) {
            if (visititem.visit === visitSelected) {
                tests.push(visititem)
            }
        }
        setTests(tests)
        
    }, [visitSelected]);

    // set visit based on user input
    const handleVisitSelected = evt => {
        const id = evt.target.value;
        setVisitSelected(id);
    };

    // create holder for form values and beginning form row
    // initialize to empty
    const [formValues, setFormValues] = React.useState([{result_plan_id: "", result_value: "", urgent: ""}])

    // add new row with empty values
    let addFormFields = () => {
        setFormValues([...formValues, {result_plan_id: "", result_value: "", urgent: ""}])
      }

    //update empty form values with input values
    let handleChange = (i, e) => {
        let newFormValues = [...formValues];
        const value =
        e.target.type === "checkbox" ? e.target.checked : e.target.value;
        newFormValues[i][e.target.name] = value;
        setFormValues(newFormValues);
      }

    // display the doctor's contact info if a result is marked as urgent
    const handleUrgentValue = e => {
        
        if (e.target.checked === true) {
            document.querySelector('#hcp_info').style.display = "";
        }
        else {
            document.querySelector('#hcp_info').style.display = "none";
        }
    }
    
    // submit all form values for visit for participant
    let handleSubmit = (event) => {
        event.preventDefault();

        const formInputs = {
            participantId : participantId,
            results : formValues
            }    
        // alert(JSON.stringify(formInputs));
        fetch('/create-result', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {'Content-Type': 'application/json',},
        })
        .then (response => {
            window.location.href =`/participants/${participantId}`;
        })
    }

    return (
        <div class="add-results basic-box">
            <div>
            <h2>Add a participant's results from a study visit</h2>
            <div class="flex-row">
                <div><h1 class="planning-num">1</h1></div>
                <div class="plan-results">
                <label><b>Study:</b></label>          
                    <select id="studyId" name="studyId" class="react-element-margin" value={studySelected} onChange={handleStudySelected}>
                        <option>Choose here</option>
                        {studies.map((data) => (
                        <option key={data.study_id} value={data.study_id}> {data.study_name}</option>
                        ))}
                    </select>
                </div>
                </div>
            </div>
            <div class="flex-row">
                <div><h1 class="planning-num">2</h1></div>
                <div class="plan-results">
                    <label><b>Participant ID:</b> </label>
                    <input type="number" class="react-element-margin" id="participantId" name="participantId" />
                    <button id="checkParticipantIdBtn" class="button medium-button react-element-margin" onClick={handleParticipantInput}>Load Study Visits</button>
                </div>    
                </div>
                <div class="flex-row">
                    <div></div>
                    <div class="plan-results" id="id_check_msg"></div>
                </div>
                 
            <div id="resultsInput" style = {{display: "none"}}>
            <div class="flex-row">
                <div><h1 class="planning-num">3</h1></div>
                <div class="plan-results">
                    <label><b>Study Visit: </b></label>
                        <select required id="visit" class="react-element-margin" name="visit" onChange={e => handleVisitSelected(e)}>
                            <option >Choose here</option>
                            {allVisits.map(visit => (
                            <option key={visit} value={visit}> {visit}</option>
                            ))}
                        </select>
                </div>
            </div>

            <div class="flex-row">
                <div><h1 class="planning-num">4</h1></div>

            <div class="plan-results flex-col">
            {/* <h4>Enter Result Info:</h4>   */}
            <table>
                <thead>
                    <tr>
                        <td width="15%"><b>Test</b></td>
                        <td width="15%"><b>Test result</b></td>
                        <td width="30%"><b>Is this urgent?</b></td>
                    </tr>
                </thead> 
                <tbody>
                {formValues.map((element, index) => (
                    <tr className="form-row" key={index}>
                        <td>
                            <select id="test" name="result_plan_id" onChange={e => handleChange(index, e)} required>
                                <option>Choose here</option>
                                {tests.map((data) => (
                                <option key={data.result_plan_id} value={data.result_plan_id}> {data.test_name}</option>
                                ))}
                            </select>
                        </td>
                        <td>
                            <input type="text" name="result_value" value={element.result_value || ""}onChange={e => handleChange(index, e)} />
                        </td>
                        <td>
                            <input type="checkbox" name="urgent" onChange={e => {
                                handleChange(index, e); 
                                handleUrgentValue(e)}}/>
                            Yes
                        </td>
                    </tr>
                ))}
                <tr>
                    <td><button className="button add medium-button" type="button" onClick={addFormFields}>Add another result for this visit</button></td>
                    <td></td>
                    <td><button className="button submit medium-button" onClick={handleSubmit}>Submit results</button></td>
                        
                </tr>
                </tbody>
            </table>
                
            </div> 
            
            </div>
            </div>
            <div id ="hcp_info"></div>
        </div>
        )}

    ReactDOM.render(<ResultsForm />, document.getElementById('results-container'));