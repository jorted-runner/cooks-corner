let cardArray = document.querySelectorAll('.card__inner');

cardArray.forEach(function(elem) {
    elem.addEventListener('click', function() {
        elem.classList.toggle('is-flipped');
    });
});

function confirmDelete(recipeId) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You won\'t be able to revert this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!',
    }).then((result) => {
        if (result.isConfirmed) {
            document.forms['deleteRecipeForm_' + recipeId].submit();
        }
    });
}


const regenButton = document.querySelector("#regenButton").addEventListener("click", regenImages);
function regenImages() {
    let imagesArray = document.querySelectorAll('.recipeImg');
    console.log(imagesArray);
}
    