document.getElementById('langBtn').addEventListener('click', function() {
    document.getElementById('langDropdown').classList.toggle('show');
});

document.querySelectorAll('.lang-dropdown a').forEach(function(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const lang = this.getAttribute('data-lang');
        window.location.href = '/set-language/' + lang;
    });
});