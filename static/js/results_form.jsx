
function ResultsForm() {
    // create form input of study names in dropdown 

    const [studies, setStudies] = React.useState([]);

    React.useEffect(() =>  {
        fetch('/studies.json')
        .then(response => response.json())
        .then(result => setStudies(result))
        }, []);
    
    const [studySelected, setStudySelected] = React.useState(null);
    const [visits, setVisits] = React.useState([]);

    React.useEffect(() => { 
        if (studySelected === null) {
            return
        }
        console.log(`Selected has changed to ${studySelected}`)
        fetch(`/visits-results.json/${studySelected}`)
        .then(response => response.json())
        .then(result => setVisits(result))
    }, [studySelected]);

    const handleStudySelected = evt => {
        const id = evt.target.value;
        console.log("handle", id);
        console.log(evt)
        setStudySelected(id);
    }

    return (
        <div>
            <form>     
                <label>select the study you will input results for</label>               
                <select id="study_id" name="study" value="I RULE" onChange={handleStudySelected}>
                    <option selected disabled>Choose here</option>
                    {studies.map((data) => (
                    <option key={data.study_id} value={data.study_id}> {data.study_name}</option>
                     ))}
                </select>
                <select id="visit" name="visit">
                    <option selected disabled>Choose here</option>
                    {visits.map((data) => (
                    <option key="{data.visit}" value="{data.visit}"> {data.visit}</option>
                     ))}
                </select>
            <div>This will be results input</div>
            </form>
        </div>        
    )
}

    ReactDOM.render(<ResultsForm />, document.getElementById('results-container'));






// function StudyInput() {  return ( <div>hello world</div> )
  
//     const [studies, setStudies] = React.useState([]);
//     const [visits, setVisits] = React.useState([]);
//     // const [results, setStudies] = React.useState([]);
  
//     React.useEffect(() =>  {
//       fetch('/studies.json')
//         .then(response => response.json())
//         .then(result => {
//           setStudies(result.studies)
//         });
//     }, []);

//     React.useEffect(() =>  {
//         fetch('/visits.json')
//           .then(response => response.json())
//           .then(result => {
//             setVisits(result.visits)
//           });
//       }, [studies]);
  
//     const studiesArray = [];
  
//     for (const currentStudy of studies) {
//       studiesArray.push(
//         <StudyInput
//           id={currentStudy.study_id}
//           name={currentStudy.study_name}
//         />
//       );
//     }
  
//     return (
//         <div className="wrapper">
//                 <form>
//            <select id={props.id} name={props.id}>
//             <option selected disabled>Choose here</option>
//             {studies.map((study.study_name, study.study_id) => (
//                 <option value="{study.study_id}" required>{study.study_name}</option>
//             ))}
            
//         </select><br></br>
//          <button type="submit">Submit</button>
//         </form>
//         </div>
//     );
//   }

// ReactDOM.render(<StudyInput />, document.getElementById('results-container'));