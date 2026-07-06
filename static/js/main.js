document.addEventListener('DOMContentLoaded', function () {
    var langBtn = document.getElementById('langBtn');
    var langDropdown = document.getElementById('langDropdown');

    if (langBtn && langDropdown) {
        langBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
        });

        document.addEventListener('click', function () {
            langDropdown.classList.remove('show');
        });
    }
});
