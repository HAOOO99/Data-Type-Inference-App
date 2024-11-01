

function DisplayTable({ data }) {
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
                        <td contentEditable='true'>{String(values[index])}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
  }

  export default DisplayTable;