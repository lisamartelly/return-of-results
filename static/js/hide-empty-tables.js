'use strict';

// hides empty tables on participants details page using the number of rows in the table
const tables = document.querySelectorAll(".pt-facing-details-table")

for (const table of tables){
    const length = table.rows.length;
    console.log("table length: ", table, length)
    if (length === 1) {
        table.innerHTML = '<li>No results will be returned</li>';
    }
}


