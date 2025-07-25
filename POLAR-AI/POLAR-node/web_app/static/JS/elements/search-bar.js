document.addEventListener("DOMContentLoaded", () => {
    const searchTablesBtn = document.getElementById("search-button-tables");
    const searchColumnsBtn = document.getElementById("search-button-columns");

    const searchTablesInput = document.getElementById("search-input-tables");
    const searchColumnsInput = document.getElementById("search-input-columns");

    if (searchTablesBtn)
        searchTablesBtn.addEventListener("click", filterTableListByName);

    if (searchColumnsBtn)
        searchColumnsBtn.addEventListener("click", filterTableContent);

    if (searchTablesInput) {
        searchTablesInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                filterTableListByName();
            }
        });
    }

    if (searchColumnsInput) {
        searchColumnsInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                filterTableContent();
            }
        });
    }
});

// ==============================
//      FILTER TABLE LIST
// ==============================

function filterTableListByName() {
    const input = document.getElementById("search-input-tables");
    const filter = input.value.toLowerCase();

    if (!table_list) return;

    const filtered = table_list.filter((tableName) =>
        tableName.toLowerCase().includes(filter)
    );

    renderTableList(filtered);
}

// ==============================
//      FILTER TABLE CONTENT
// ==============================

function filterTableContent() {
    const input = document.getElementById("search-input-columns");
    const filter = input.value.toLowerCase();

    if (!table_content || !Array.isArray(table_content)) return;

    const filtered = table_content.filter(row => {
        return Object.values(row).some(val => {
            return String(val).toLowerCase().includes(filter);
        });
    });

    // obtenemos el nombre actual de la tabla
    const tableName = document.getElementById("table-title").textContent;

    const order = headers && headers.length > 0
        ? headers
        : [];

    renderTableContent(tableName, filtered, order);
}

