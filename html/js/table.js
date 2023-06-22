const toplayer_class = 'region';
var tbls_orders = {};

var children = document.querySelectorAll('th');
children.forEach((child) => {
    child.addEventListener("click", tblSortClickHandler);
});


function tblSortClickHandler(event) {
    var child = event.srcElement;
    var parent = child.parentNode;

    var index = Array.prototype.indexOf.call(parent.children, child);
    var parent_id = parent.parentNode.parentNode.id;
    sortCol(parent_id, index);
}

function sortCol(tbl_id, tbl_col) {
    var dir = getTableSortOrder(tbl_id, tbl_col);
    sortTopLevels(tbl_id, '', tbl_col, dir);
}

function createTblHead(id, data) {
    const tHead = document.createElement("thead");
    const myCurrentRow = document.createElement("tr");

    for (let i = 0; i < data.length; i++) {
        const myCurrentCell = document.createElement("th");
        const currentText = document.createTextNode(data[i]);
        myCurrentCell.appendChild(currentText);
        myCurrentCell.addEventListener("click", function () {
            sortTable(id, i);
        });

        myCurrentRow.appendChild(myCurrentCell);
    }
    tHead.appendChild(myCurrentRow);
    return tHead;
}

function createTbl(id, head, data, parent_id = null) {

    const myTable = document.createElement("table");
    myTable.id = id;
    tHead = createTblHead(myTable.id, head);
    tbls_orders[myTable.id] = [-1, -1];

    myTable.appendChild(tHead);

    for (var d in data) {
        const parent = data[d][0][0];
        const tableBody = document.createElement("tbody");
        tableBody.id = parent;
        tableBody.className = 'region';
        tableBody.dataset.parent = 'region';
        tableBody.addEventListener("click", toggleView);
        createRow(tableBody, [data[d][0]], true);

        const subTableBody = document.createElement("tbody");
        subTableBody.dataset.parent = parent;
        createRow(subTableBody, data[d][1], false, parent + '_child');
        subTableBody.style.display = 'none';

        myTable.appendChild(tableBody);
        myTable.appendChild(subTableBody);
    }

    if (parent_id === null) {
        document.body.appendChild(myTable);
    } else {
        parent = document.getElementById(parent_id);
        parent.appendChild(myTable);
}
}

function createRow(tbody, data, fl = false, dataParent = '') {
    for (let j = 0; j < data.length; j++) {
        // creates a <tr> element
        const currentRow = document.createElement("tr");
        currentRow.dataset.parent = dataParent;

        for (let i = 0; i < data[j].length; i++) {
            // creates a <td> element
            const currentCell = document.createElement("td");
            // creates a Text Node

            if (!fl && i === 0) {
                currentCell.style = 'padding-left: 56px;';
                //currentCell.className = 'hide';
            }

            //"└── ├──"


            if (fl && i === 0) {
                const currentText = document.createTextNode(data[j][i]);
                const currentSpan = document.createElement("span");
                currentSpan.className = "caret";
                currentSpan.appendChild(currentText);
                currentCell.appendChild(currentSpan);
            } else {

                const currentText = document.createTextNode(data[j][i]);
                // appends the Text Node we created into the cell <td>
                currentCell.appendChild(currentText);
            }
            // appends the cell <td> into the row <tr>
            currentRow.appendChild(currentCell);
        }
        // appends the row <tr> into <tbody>
        tbody.appendChild(currentRow);
}
}

function toggleView(event) {
    var parent = event.currentTarget.parentElement;
    var tbody = parent.querySelectorAll("[data-parent='" + this.id + "']")[0];
    tbody.style.display = ((tbody.style.display != 'none') ? 'none' : '');

    var span = event.currentTarget.querySelector("span");
    span.classList.toggle("caret-down");

}

function getTableSortOrder(tbl_id, col_num) {
    var dir = '';
    if (tbls_orders[tbl_id] === undefined) {
        tbls_orders[tbl_id] = [-1, -1];

    }

    if (tbls_orders[tbl_id][0] !== col_num) {
        dir = 'asc';
    } else {
        dir = (tbls_orders[tbl_id][1] === 'asc') ? 'desc' : 'asc';
    }
    tbls_orders[tbl_id][0] = col_num;
    tbls_orders[tbl_id][1] = dir;
    return dir;
}

function sortTable(id, col) {
    var dir = getTableSortOrder(id, col);

    sortTopLevels(id, toplayer_class, col, dir);
    regions = getElementsToSort(id, toplayer_class);
    for (var r in regions) {

        sortTopLevels(id, regions[r].id + "_child", col, dir);
        tbody = document.querySelectorAll("[data-parent='" + regions[r].id + "']")[0];
        regions[r].parentNode.insertBefore(tbody, regions[r].nextSibling);
    }
}

function getElementsToSort(tbl_id, dataParent) {
    table = document.getElementById(tbl_id);
    rows = table.rows;
    elements_to_sort = [];

    for (i = 1; i < (rows.length); i++) {

        if (rows[i].parentElement.dataset.parent === dataParent) {
            elements_to_sort.push(rows[i].parentElement);
        } else if (rows[i].dataset.parent === dataParent) {
            elements_to_sort.push(rows[i]);
        } else if (dataParent === '') {
            elements_to_sort.push(rows[i]);
        }

    }
    return elements_to_sort;
}

function sortTopLevels(id, className, col, dir) {
    var i, rows, shouldSwitch, switchcount = 0;
    var switching = true;
    //dir = "asc";
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = getElementsToSort(id, className);
        for (i = 0; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
             one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[col];
            y = rows[i + 1].getElementsByTagName("TD")[col];
            console.log(x.innerHTML.toLowerCase() + "::" + y.innerHTML.toLowerCase());

            if (isNaN(x.innerHTML)) {
                console.log(x.innerHTML + " is not a number <br/>");
                x = x.innerHTML.toLowerCase();
                y = y.innerHTML.toLowerCase();
            } else {
                console.log(x.innerHTML + " is a number <br/>");
                x = Number(x.innerHTML);
                y = Number(y.innerHTML);
            }

            if (dir === "asc") {
                if (x > y) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (x < y) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
             and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount++;
        }
    }
}
