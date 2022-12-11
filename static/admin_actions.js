function newRecord() {
    const table = document.querySelector(".show.active").querySelector("table");
    const numOfRows = table.rows[0].children.length;
    
    // Reads table column names in array
    const headers = table.rows[0].children;
    console.log(headers);
    allHeaders = [];
    for (header of headers) {
        allHeaders.push(header.innerHTML);
    }
    console.log(allHeaders);

    const newRow = document.createElement("tr");
    for (let i = 0; i < numOfRows; i++) {
        const newCell = document.createElement("td");
        newCell.innerHTML = `<input class='form-control' name=${allHeaders[i]} placeholder='${allHeaders[i]}'>`;
        newRow.append(newCell);
    }
    table.append(newRow);
}