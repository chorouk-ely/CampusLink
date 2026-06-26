function filterSemestre(semestre) {
    const url = new URL(window.location.href);
    url.searchParams.set('semestre', semestre);
    window.location.href = url.toString();
}