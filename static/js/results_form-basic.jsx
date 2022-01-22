
function ResultsForm() {
    // create form input of study names in dropdown 
    
    const [studies, setStudies] = React.useState([]);
    React.useEffect(() =>  {
        fetch('/studies.json')
        .then(response => response.json())
        .then(result => setStudies(result))
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

    const handleVisitSelected = evt => {
        const id = evt.target.value;
        setVisitSelected(id);
    }
    
    // render form html
    return (
        <div>
            <label>select the study you will input results for</label>               
                <select id="study_id" name="study" onChange={handleStudySelected}>
                    <option>Choose here</option>
                    {studies.map((data) => (
                    <option key={data.study_id} value={data.study_id}> {data.study_name}</option>
                     ))}
                </select>
                
            <table>
                <thead>
                    <tr>
                        <th>participant ID</th>
                        <th>study visit</th>
                        <th>test</th>
                        <th>test result</th>
                        <th>is this urgent?</th>
                    </tr>
                </thead> 
                <tbody> 
                    <tr>
                        <td>
                            <input type="number" name="participant-id" required/>   
                        </td>
                        <td>
                            <select id="visit" name="visit" onChange={handleVisitSelected} required>
                                <option >Choose here</option>
                                {allVisits.map(visit => (
                                <option key={visit} value={visit}> {visit}</option>
                                ))}
                            </select>
                        </td>
                        <td>
                            <select id="test" name="test" required>
                                <option>Choose here</option>
                                {tests.map((data) => (
                                <option key={data.result_plan_id} value={data.result_plan_id}> {data.test_name}</option>
                                ))}
                            </select>
                        </td>
                        <td>
                            <input type="text" name="result-value" />
                        </td>
                        <td>
                            <input type="checkbox" name="urgency"/>
                        </td>
                    </tr>
                </tbody>  
            </table>

            <button>Submit</button>
            <button>Add more</button>
        </div>        
    )
}

    ReactDOM.render(<ResultsForm />, document.getElementById('results-container'));