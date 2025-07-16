// Función para obtener la lista de bots desde la API
async function fetchBots() {

    response = await send_API_request("POST", "/api/get-models", null)
    
    if (!response.ok) {
        // console.log("error right here")
        const errorData = await response.json();
        alert(errorData.message || 'ERROR: bots could not be loaded');
        return;
    }
    //console.log("response: ", response)
    const data = await response.json();
    chat_displayBots(data.bots);
}

// Función para insertar los bots en el HTML como divs
function chat_displayBots(bots) {
    const container = document.getElementById('bots-container'); 

    // Limpia el contenedor antes de agregar nuevos elementos
    container.innerHTML = '';

    if (bots.length === 0) {
        // Si no hay bots, muestra un mensaje
        container.innerHTML = '<p>No tienes bots disponibles.</p>';
        return;
    }

    // Recorre la lista de bots y crea un div para cada uno
    bots.forEach(bot => {
        const botDiv = document.createElement('div');
        botDiv.classList.add('bot-card');
        botDiv.innerHTML = `
            <h3>${bot}</h3>
        `;
    
        // Agregar el manejador de eventos para redirigir al usuario
        botDiv.addEventListener('click', () => {
            // Construir la URL con el nombre del bot como parámetro
            goToModelChat(bot)
        });
    
        // Agregar el div creado al contenedor
        container.appendChild(botDiv);
    });
}
