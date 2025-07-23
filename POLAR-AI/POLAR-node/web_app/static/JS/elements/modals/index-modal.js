document.getElementById('database-card').onclick = async function () {
    try {
        const response = await send_API_request('GET', '/sites/database');

        if (response.ok) {
            loadPage(response.url);
        }
    } catch (error) {
        console.error("Error accediendo a /sites/database:", error);
        alert("Error al intentar acceder a la página.");
    }
};
