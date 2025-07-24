
let table_list;
let table_content;
let selectedRowData = null;

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
    
    if (data) {
        table_list = data.tables || [];
        renderTableList(data.tables);
    }
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
        table_content = response.content.data;
        renderTableContent(tableName, response.content.data, headers);
    } else {
        renderTableContent(tableName, [], []);
    }
}

// ==============================
//      RENDER TABLE CONTENT
// ==============================

function renderTableContent(tableName, content, headers) {
    const titleEl = document.getElementById("table-title");
    const tableEl = document.getElementById("table-content");

    titleEl.textContent = tableName;
    tableEl.innerHTML = "";

    if (!Array.isArray(content) || content.length === 0) {
        tableEl.innerHTML = "<tr><td>No data available</td></tr>";
        return;
    }

    // create table headers
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
        tr.id = row["id"];

        tr.addEventListener("click", () => {
            // remove class "selected" from all rows
            const allRows = tbody.querySelectorAll("tr");
            allRows.forEach(r => r.classList.remove("selected"));

            // add class "selected" to the clicked row
            tr.classList.add("selected");

            // save data
            selectedRowData = row;

            // show JSON data in the viewer
            const viewer = document.getElementById("json-viewer");
            viewer.innerHTML = syntaxHighlight(row);

            const copyBtn = document.getElementById("copy-json-btn");
            copyBtn.onclick = () => copyJSONToClipboard(row);
        });

        headers.forEach((key) => {
            const td = document.createElement("td");
            td.textContent = row[key];
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });
    tableEl.appendChild(tbody);
}

// ==============================
//      JSON viewer functions
// ==============================

function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, null, 2);
    }

    json = json
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(?:\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, (match) => {
        let cls = 'json-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'json-key';
            } else {
                cls = 'json-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'json-boolean';
        } else if (/null/.test(match)) {
            cls = 'json-null';
        }
        return `<span class="${cls}">${match}</span>`;
    });
}

function copyJSONToClipboard(jsonObj) {
    const text = JSON.stringify(jsonObj, null, 2);
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById("copy-json-btn");
        const originalText = btn.textContent;
        btn.textContent = "✔️";
        setTimeout(() => {
            btn.textContent = originalText;
        }, 1500);
    }).catch(err => {
        console.error("Error al copiar:", err);
    });
}

// ==============================
//      SEARCH FUNCTIONALITY
// ==============================

