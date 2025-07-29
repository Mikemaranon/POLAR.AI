const input = document.getElementById('command-input');
const output = document.getElementById('output-container');
const terminal = document.getElementById('terminal');

const welcome_msg = [
 
    "  ____________________________________________________________",
    " |        ___  ____  __   ___   ___        ___   ____         |",
    " |       / _ \\/ __ \\/ /  / _ | / _ \\      / _ | /  _/         |",
    " |      / ___/ /_/ / /__/ __ |/ , _/ _   / __ |_/ /           |",
    " |     /_/   \\____/____/_/ |_/_/|_| (_) /_/ |_/___/           |",
    " |                                                            |",
    " |                                                            |",
    " |      Welcome to POLAR Shell! Type your commands below      |",
    " |____________________________________________________________|\n"
]

// wellcome message
function printWelcome() {
    output.innerHTML = welcome_msg.join("\n") + "\n";
    scrollToBottom();
}

// soft scroll to the bottom of the terminal
function scrollToBottom() {
    output.scrollTop = output.scrollHeight;
}

// prints the message from the server
function printMsg(data) {
    try {
        const parsed = JSON.parse(data);
        const outputArray = parsed.output;

        if (!Array.isArray(outputArray) || outputArray.length < 1) {
            return "Invalid response.";
        }

        return outputArray[1] !== null ? outputArray[1] : outputArray[0];
    } catch (err) {
        return "Error processing response.";
    }
}


// Enter
input.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
        const command = input.value.trim();
        if (!command) return;

        // Mostrar el comando
        output.innerHTML += `$ ${command}\n`;
        input.value = "";

        try {
            const res = await send_API_request('POST', "/api/shell/execute", { "command": command });

            const data = await res.text();
            output.innerHTML += `${printMsg(data)}\n\n`;
        } catch (err) {
            output.innerHTML += `Error running command.\n\n`;
        }

        scrollToBottom();
    }
});

// Automatically focus the input when clicking anywhere
document.addEventListener('click', () => {
    input.focus();
});

// Initialize the terminal
printWelcome();
input.focus();