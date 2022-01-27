
function ResultsForm() {
    // learned a lot from this: https://bapunawarsaddam.medium.com/add-and-remove-form-fields-dynamically-using-react-and-react-hooks-3b033c3c0bf5
    
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
            console.log(responseData)
            if (responseData.code === 1) {
                document.querySelector('#resultsInput').style.display = "";
            }
            else if (responseData.code === 0) {
                document.querySelector('#resultsInput').style.display = "none";
            }
        })
    }, [participantId]);

    const handleParticipantInput = evt => {
        const id = document.querySelector('#participantId').value;
        setParticipantId(id);
    }

    React.useEffect(() => {
        console.log("loaded!!!")
        const urlParams = new URLSearchParams(window.location.search);
        setParticipantId(urlParams.get('participantId'));
        setStudySelected(urlParams.get('studyId'));
        document.getElementById('studyId').value = urlParams.get('studyId')
        document.getElementById('participantId').value = urlParams.get('participantId')
        }, []);

    // create test input based on selected visit
    const [visitSelected, setVisitSelected] = React.useState(null);
    const [tests, setTests] = React.useState([]);

    React.useEffect(() => { 
        console.log("test use Effect", visitSelected)
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

    const handleVisitSelected = evt => {
        const id = evt.target.value;
        setVisitSelected(id);
    }

    const [formValues, setFormValues] = React.useState([{result_plan_id: "", result_value: "", urgent: ""}])

    let addFormFields = () => {
        setFormValues([...formValues, {result_plan_id: "", result_value: "", urgent: ""}])
      }

    let handleChange = (i, e) => {
        let newFormValues = [...formValues];
        const value =
        e.target.type === "checkbox" ? e.target.checked : e.target.value;
        newFormValues[i][e.target.name] = value;
        setFormValues(newFormValues);
      }

    
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
        <div>
            <div>
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
                <input type="text" id="participantId" name="participantId" />
                <div id="id_check_msg"></div>
                <button id="checkParticipantIdBtn" onClick={handleParticipantInput}>Next</button>
            </div> 
            <div id="resultsInput" style = {{display: "none"}}>
            <label>Study Visit: </label>
                <select required id="visit" name="visit" onChange={e => {
                    handleVisitSelected(e);
                    }}>
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
                            <input type="checkbox" name="urgent" onChange={e => handleChange(index, e)} />
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