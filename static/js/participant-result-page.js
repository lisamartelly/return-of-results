'use strict';

const tables = document.querySelectorAll(".result-table")

for (const table of tables){
    const length = table.rows.length;
    console.log("table length: ", table, length)
    if (length === 1) {
        table.innerHTML = '<li>No results will be returned during this time period</li>';
    }
}

const displayUrgentResults = () => {
    fetch()
}
