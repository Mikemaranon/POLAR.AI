const checkbox = document.getElementById('theme-toggle-checkbox');
const body = document.body;

// Load prefference
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark');
    checkbox.checked = true;
}

// Theme toggle
checkbox.addEventListener('change', function () {
    if (this.checked) {
        body.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    }
});
