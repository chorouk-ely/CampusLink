// Filter student dropdown based on selected class
function filterEtudiants(classeChoisie) {
    const etudiantSelect = document.getElementById('etudiantSelect');
    const options = etudiantSelect.querySelectorAll('option[data-classe]');

    // Reset selection
    etudiantSelect.value = '';

    options.forEach(function (option) {
        if (classeChoisie === '' || option.getAttribute('data-classe') === classeChoisie) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

// Auto-hide success alert after 4 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(function (alert) {
    setTimeout(function () {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
});