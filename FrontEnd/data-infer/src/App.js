import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import React from 'react';
import { useState ,useRef} from 'react';
import DisplayTable from './DisplayTable';

import './App.css';

function App() {

  const [result,setResult] = useState("");
  const [flag, setFlag] = useState(false);
  const [type,setType] = useState("");
  const [prevType,setPrevType] = useState("");
  

  const handleDataChange = updatedData => {
    setResult(updatedData);  // Set the result state
    setType(Object.values(updatedData));  // Perform additional actions
  };

  // Create a reference to the hidden file input element
  const hiddenFileInput = useRef(null);
  
  // handler for the data type override
  const submitData = async (result,type) => {
      // setType(Object.values(result))

      console.log(prevType);
      console.log(type)
      console.log(result)
      
      const data = {
        'result':result,
        'keys':prevType,
        'newValues':type
      }

      const url = 'http://localhost:8000/api/submit/';  // Update with your actual backend API URL
      const options = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      };
      
      try {
          const response = await fetch(url, options);
          const data = await response.json();
          setResult(data);
          console.log('Submission successful:', data);
          alert('Data submitted successfully!');
      } catch (error) {
          console.error('Submission failed:', error);
          alert('Failed to submit data.');
      }
  };
  
  // Handler to simulate file input click when button is clicked
  const handleClick = () => {
    hiddenFileInput.current.click();
    // console.log(hiddenFileInput)
  };
  // Handler for file selection
  const handleChange = async (event) => {
    const fileUploaded = event.target.files[0];
    if (fileUploaded) {
      // Check if the file is a CSV or Excel file
      const fileType = fileUploaded.type;
      const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']; // MIME types for CSV and Excel files
      if (validTypes.includes(fileType)) {
          console.log('Uploading file:', fileUploaded.name);

          const formData = new FormData();
          formData.append('file', fileUploaded);

          try {
              const response = await fetch('http://localhost:8000/api/upload/', {
                  method: 'POST',
                  body: formData,
              });
              const res = await response.json();
              console.log(res);
              setResult(JSON.parse(res.message));
              setType(Object.values(JSON.parse(res.message)));
              setPrevType(res.origin)
              setFlag(true);
              
              alert('File uploaded successfully!');
          } catch (error) {
              console.error('Error uploading file:', error);
              alert('Failed to upload file.');
          }
      } else {
          alert('Please upload a CSV or Excel file.');
      }
  }
  
};
  return (
    <div className="App">
      <Container className="d-flex justify-content-center align-items-center" 
                style={{ height: '50vh' }}> 
        {/* <Stack gap={2}> */}

          <Button variant="info"onClick={handleClick}>Import Excel/CSV file</Button>{' '}

          <input
                type="file"
                ref={hiddenFileInput}
                onChange={handleChange}
                accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" // Filters to only allow CSV and Excel files
                style={{ display: 'none' }} // Hide the file input
            />
            <hr></hr>

            {flag && <DisplayTable data={result} onDataChange={handleDataChange} /> }
            {flag && <Button variant="info" onClick={()=>submitData(result,type)}>Submit</Button>}
        {/* </Stack> */}
        

      </Container>
      
    </div>
  );
}

export default App;
