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
    let recipeTitle = document.querySelector("#displayTitle");
    let recipeDesc = document.querySelector("#displayDesc");
    let recipeIngredients = document.querySelector("#displayIngredients");
    console.log(recipeTitle, recipeDesc, recipeIngredients)
    let imagesArray = document.querySelectorAll('.recipeImg');
    $.ajax({
        url: '/regen_images',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'title': recipeTitle , 'desc': recipeDesc, 'ingredients': recipeIngredients}),
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
    