// Function to open the modal
function openModal(renderModal) {
    const modal = document.getElementById("myModal");
    const fadeBackground = document.getElementById("fadeBackground");

    // Muestra el fondo opaco y el modal
    fadeBackground.style.display = "block";
    modal.style.display = "block";

    // Agrega las clases 'show' para la animación
    setTimeout(() => {
        fadeBackground.classList.add('show'); // Animar el fondo con fundido
        modal.classList.add('show'); // Animar el modal con deslizamiento
    }, 10); // Pequeño retraso para asegurar que el estilo se aplique correctamente
    
    if (typeof renderModal === 'function') {
        renderModal();
    }
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById("myModal");
    const fadeBackground = document.getElementById("fadeBackground");

    // Quitar las clases 'show' para cerrar el modal y fondo
    modal.classList.remove('show');
    fadeBackground.classList.remove('show');

    // Después de la animación, ocultamos el modal y fondo
    setTimeout(() => {
        modal.style.display = "none"; // Ocultar el modal
        fadeBackground.style.display = "none"; // Ocultar el fondo
    }, 300); // Debe coincidir con el tiempo de la transición en CSS
}

// Close modal when clicking outside of the modal content
window.onclick = function(event) {
    const modal = document.getElementById("myModal");
    const fadeBackground = document.getElementById("fadeBackground");

    if (event.target == fadeBackground) {  // click outside
        closeModal(); // Close modal
    }
}
