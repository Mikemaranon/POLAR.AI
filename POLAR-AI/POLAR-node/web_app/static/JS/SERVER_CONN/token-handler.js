
async function login(username, password) {
    const endpoint = "/login";
    if (!username || !password) {
        throw new Error("Username and password are required.");
    }

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
    };

    console.log("loging... :", endpoint, options);

    try {
        const response = await fetch(endpoint, options);

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }
        return response;
    } catch (error) {
        console.error("Error in API request:", error);
        throw error;
    }
}

async function send_API_request(method, endpoint, body = null) {

    const options = {
        method: method.toUpperCase(),
        headers: {
            "Content-Type": "application/json",
        },
        credentials: 'include'
    };
    
    if (body && method.toUpperCase() !== "GET") {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(endpoint, options);

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }
        return response;
    } catch (error) {
        console.error("Error in API request:", error);
        throw error;
    }
}

async function logout() {
    const endpoint = "/logout";

    const options = {
        method: "POST",
        credentials: 'include'
    };

    try {
        const response = await fetch(endpoint, options);

        if (!response.ok) {
            throw new Error(`Logout failed: ${response.status}`);
        }
        return response;
    } catch (error) {
        console.error("Error during logout:", error);
        throw error;
    }
}

async function loadPage(url) {
    try {
        window.location.href = url
    } catch (error) {
        console.error("Error loading page:", error);
        // window.location.href = "/login";
    }
}