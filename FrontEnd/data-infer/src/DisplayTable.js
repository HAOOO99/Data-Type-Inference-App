
function DisplayTable({ data, onDataChange }) {
    const handleDataChange = (event, key) => {
      // const storedData = {...data};
      // const storedType = Object.values(storedData);
      // console.log(storedType);

      const updatedData = {...data};
      
      updatedData[key] = event.target.value;
      console.log("check update",key, updatedData[key]);

      onDataChange(updatedData);  // Pass the updated data back to the parent component
    };

    const keys = Object.keys(data);
    const values = Object.values(data);
    return (
      <table id="editableTable"  className="table w-75">
            <thead>
                <tr>
                    <th>Column </th>
                    <th>Inferred Data Type</th>
                </tr>
            </thead>
            <tbody>
                {keys.map((key, index) => (
                    <tr key={index}>
                        <td className="fst-italic">{key}</td>
                        {/* <td contentEditable='true' 
                            onChange={e => handleDataChange(e, index)}>
                              {String(values[index])}</td> */}
                              <td >
                              <input
                                type="type"
                                value={String(values[index])}
                                onChange={(e) => handleDataChange(e, key)}
                            />
                              </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
  }

  export default DisplayTable;