async function handleLoginSubmit(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    try {
        const response = await login(username, password)

        if (!response.ok) {
            const text = await response.text().trim();
            errorMessage.textContent = text || "Error in servers response";
            errorMessage.style.display = "block";
            return;
        } else {
            loadPage("/");
        }
    } catch (error) {
        console.error("Error during login:", error);
        errorMessage.textContent = "Incorrect user, please try again.";
        errorMessage.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    
    loginForm.addEventListener("submit", handleLoginSubmit);
});