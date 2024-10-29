import Button from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Container from 'react-bootstrap/Container';
import React from 'react';

// import './App.css';

function App() {

  // Create a reference to the hidden file input element
  const hiddenFileInput = React.useRef(null);

  // Handler to simulate file input click when button is clicked
  const handleClick = () => {
    hiddenFileInput.current.click();
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
              const result = await response.json();
              console.log(result);
              alert('File uploaded successfully!');
          } catch (error) {
              console.error('Error uploading file:', error);
              alert('Failed to upload file.');
          }
          // Process your file here (e.g., read file, upload to server)
      } else {
          alert('Please upload a CSV or Excel file.');
      }
  }
    // console.log(postfix); // Do something with the uploaded file
};
  return (
    <div className="App">
      <Container className="d-flex justify-content-center align-items-center" 
                style={{ height: '50vh' }}> 
        {/* <Stack gap={2}> */}

          <Button variant="info"onClick={handleClick}>Import Excel/CSV file</Button>{' '}
        {/* </Stack> */}
        <input
                type="file"
                ref={hiddenFileInput}
                onChange={handleChange}
                accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" // Filters to only allow CSV and Excel files
                style={{ display: 'none' }} // Hide the file input
            />

      </Container>
      
    </div>
  );
}

export default App;
