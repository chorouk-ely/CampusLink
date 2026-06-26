// Toggle password form visibility
function togglePasswordForm() {
    const form = document.getElementById('passwordForm');
    form.classList.toggle('visible');
}

// Auto-open form if there's an error (so user sees what went wrong)
window.addEventListener('DOMContentLoaded', function () {
    const hasAlert = document.querySelector('.alert-error');
    if (hasAlert) {
        const form = document.getElementById('passwordForm');
        if (form) form.classList.add('visible');
    }
});

// Auto-hide alerts after 4 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(function (alert) {
    setTimeout(function () {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
});