const checkbox = document.getElementById('theme-toggle-checkbox');
 const themeStyle = document.getElementById('theme-style');

// Load prefference
if (localStorage.getItem('theme') === 'dark') {
    themeStyle.setAttribute('href', "/static/CSS/themes/dark-theme.css");
    checkbox.checked = true;
}

// Theme toggle
checkbox.addEventListener('change', function () {
    if (this.checked) {
        themeStyle.setAttribute('href', "/static/CSS/themes/dark-theme.css");
        localStorage.setItem('theme', 'dark');
    } else {
        themeStyle.setAttribute('href', "/static/CSS/themes/bright-theme.css");
        localStorage.setItem('theme', 'light');
    }
});
