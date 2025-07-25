const input = document.getElementById('command-input');
const output = document.getElementById('output-container');
const terminal = document.getElementById('terminal');

const welcome_msg = [
    "  _____   ____  _               _____                 _____  ",
    " |  __ \ / __ \| |        /\   |  __ \          /\   |_   _| ",
    " | |__) | |  | | |       /  \  | |__) |        /  \    | |   ",
    " |  ___/| |  | | |      / /\ \ |  _  /        / /\ \   | |   ",
    " | |    | |__| | |____ / ____ \| | \ \   _   / ____ \ _| |_  ",
    " |_|     \____/|______/_/    \_\_|  \_\ (_) /_/    \_\_____| "
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
            output.innerHTML += `${data.trim()}\n\n`;
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
// printWelcome();
input.focus();