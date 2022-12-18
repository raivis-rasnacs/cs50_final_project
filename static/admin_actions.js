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
    newRow.insertAdjacentHTML("beforeend", `<td></td>`);
    for (let i = 1; i < numOfRows; i++) {
        const newCell = document.createElement("td");
        newCell.innerHTML = `<input class='form-control' name=${allHeaders[i]} placeholder='${allHeaders[i]}'>`;
        newRow.append(newCell);
    }
    table.append(newRow);
}

function saveChanges() {
    const activeTab = document.querySelector('a[aria-selected="true"]').getAttribute("aria-controls");
    const table = document.getElementById(activeTab + "-table");
    saveState(table);

    // Reads table in object
    var tableData = {};
    for (let i = 1; i < table.rows.length; i++) {
        tableData[table.rows[i].cells[0].innerHTML] = {} 
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            tableData[table.rows[i].cells[0].innerHTML][table.rows[0].cells[j].innerHTML] = table.rows[i].cells[j].innerHTML;
        }
    }
    
    fetch("/admin/save",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
            'dataToSave' : tableData,
            'table' : activeTab,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        location.reload()
    })
}

function saveState(table) {
    for (let i = 1; i < table.rows.length; i++) {
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            var activeCell = table.rows[i].cells[j];
            var inputField = activeCell.querySelector("input");
             if (inputField != null) {
                var cellValue = inputField.value;
                inputField.remove();
                activeCell.insertAdjacentHTML("beforeend", `${cellValue}`);
             }
        }
    }
}