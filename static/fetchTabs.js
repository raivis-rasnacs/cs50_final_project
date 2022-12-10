function fetchData(selectedTabName) {
    fetch("/admin/data",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
            'selectedTab' : selectedTabName
        })
    })
    .then(response => response.json())
    .then(data => {
        showContent(data["data"], selectedTabName);
    })
}


function showContent(data, selectedTabName) {
    const table = document.getElementById(selectedTabName+'-table');
    clearTable(table)

    for (record of data) {
        const row = document.createElement("tr");
        for (column of record) {
            const cell = document.createElement("td");
            cell.textContent = column;
            row.append(cell);
        }
        table.append(row);
    }
}

function clearTable(table) {
    while (table.rows.length > 1) {
        table.rows[1].remove();
    }
}