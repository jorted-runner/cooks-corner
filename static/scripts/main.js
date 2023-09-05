let cardArray = document.querySelectorAll('.card__inner');

cardArray.forEach(function(elem) {
    elem.addEventListener('click', function() {
        elem.classList.toggle('is-flipped');
    });
});