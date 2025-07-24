
// ==============================
//         ON LOAD EVENT
// ==============================

document.addEventListener("DOMContentLoaded", () => {
    loadTableList();
});

async function getData(method, endpoint, body = null) {
    try {
        const res = await send_API_request(method, endpoint, body);
        return await res.json();
    } catch (error) {
        console.error("Error getting data:", error);
        return null;
    }
}

// ==============================
//      LOAD TABLE LIST
// ==============================

async function loadTableList() {
    const data = await getData("GET", "/api/db/tables");
    if (data) renderTableList(data.tables);
}

// ==============================
//      RENDER TABLE LIST
// ==============================

function renderTableList(tables) {
    const listElement = document.getElementById("table-list");
    listElement.innerHTML = "";

    tables.forEach((tableName) => {
        const li = document.createElement("li");
        li.textContent = tableName;
        li.classList.add("table-item");
        li.style.cursor = "pointer";
        li.addEventListener("click", () => loadTableContent(tableName));
        listElement.appendChild(li);
    });
}

// ==============================
//      LOAD TABLE CONTENT
// ==============================

async function loadTableContent(tableName) {
    const response = await getData("POST", `/api/db/table-content`, { "table_name": tableName });
    if (response && response.content && Array.isArray(response.content.data)) {
        console.log(response.content.columns);
        const headers = response.content.columns.map(col => col.name);
        renderTableContent(tableName, response.content.data, headers);
    } else {
        renderTableContent(tableName, []);
    }
}


// ==============================
//      RENDER TABLE CONTENT
// ==============================

function renderTableContent(tableName, content) {
    const titleEl = document.getElementById("table-title");
    const tableEl = document.getElementById("table-content");

    titleEl.textContent = tableName;
    tableEl.innerHTML = "";

    if (!Array.isArray(content) || content.length === 0) {
        tableEl.innerHTML = "<tr><td>No data available</td></tr>";
        return;
    }

    // create table headers
    const headers = Object.keys(content[0]);
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    headers.forEach((key) => {
        const th = document.createElement("th");
        th.textContent = key;
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    tableEl.appendChild(thead);

    // create table body
    const tbody = document.createElement("tbody");
    content.forEach((row) => {
        const tr = document.createElement("tr");
        headers.forEach((key) => {
        const td = document.createElement("td");
        td.textContent = row[key];
        tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    tableEl.appendChild(tbody);
}



