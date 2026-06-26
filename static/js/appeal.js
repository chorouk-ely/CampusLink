// Auto-resize textarea as user types
const textarea = document.querySelector('.appeal-textarea');
if (textarea) {
    textarea.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
}

// Confirm before sending
const form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', function (e) {
        const select = document.querySelector('.appeal-select');
        const message = document.querySelector('.appeal-textarea');

        if (!select.value) {
            e.preventDefault();
            alert('Veuillez sélectionner un professeur.');
            return;
        }

        if (message.value.trim().length < 10) {
            e.preventDefault();
            alert('Votre message est trop court (minimum 10 caractères).');
            return;
        }
    });
}

// Auto-hide alerts after 4 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(function (alert) {
    setTimeout(function () {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
});