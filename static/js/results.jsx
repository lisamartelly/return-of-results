
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
            console.log(responseData)
            document.querySelector('#id_check_msg').innerHTML = responseData.msg;
            if (responseData.code === 1) {
                document.querySelector('#resultsInput').style.display = "";
                document.querySelector('#hcp_info').style.display = "none";
                document.querySelector('#hcp_info').innerHTML = `
                <h3>Participant's HCP Contact Info:</h3>
                <p>HCP Full Name: ${responseData.hcp_phone} </p>
                <p>HCP Phone: ${responseData.hcp_phone} </p>
                <p>HCP Email: ${responseData.hcp_email} </p>
                <p>HCP Practice: ${responseData.hcp_practice} </p>
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
        console.log("TESTS: ", tests)
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

    const handleUrgentValue = e => {
        console.log("e.target.checked", e.target.checked);
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
        alert(JSON.stringify(formInputs));
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
        <div>
            <div>
            <div id ="hcp_info"></div>
            <h4>Select Study, Study Visit, and Enter Participant ID:</h4>  
                <label>Select Study:</label>               
                    <select id="studyId" name="studyId" value={studySelected} onChange={handleStudySelected}>
                        <option>Choose here</option>
                        {studies.map((data) => (
                        <option key={data.study_id} value={data.study_id}> {data.study_name}</option>
                        ))}
                    </select>
            </div>
            <div>
                <label>Participant ID: </label>
                <input type="number" id="participantId" name="participantId" />
                <button id="checkParticipantIdBtn" onClick={handleParticipantInput}>Load Study Visits</button>
                <div id="id_check_msg"></div>
            </div> 
            <div id="resultsInput" style = {{display: "none"}}>
            <label>Study Visit: </label>
                <select required id="visit" name="visit" onChange={e => handleVisitSelected(e)}>
                    <option >Choose here</option>
                    {allVisits.map(visit => (
                    <option key={visit} value={visit}> {visit}</option>
                    ))}
                </select>

            <h4>Add Results For This Study Visit:</h4>  
            <table>
                <thead>
                    <tr>
                        <th>test</th>
                        <th>test result</th>
                        <th>is this urgent?</th>
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
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
                <button className="button add" type="button" onClick={addFormFields}>Add</button>
                <button className="button submit" onClick={handleSubmit}>Submit</button>
                <div id="update-success"></div>
            </div> 
        </div>
        )}

    ReactDOM.render(<ResultsForm />, document.getElementById('results-container'));