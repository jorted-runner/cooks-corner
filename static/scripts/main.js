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
    let recipeTitle = document.querySelector("#displayTitle").value;
    let recipeDesc = document.querySelector("#displayDesc").value;
    let recipeIngredients = document.querySelector("#displayIngredients").value;
    console.log(recipeTitle, recipeDesc, recipeIngredients)
    let imagesArray = document.querySelectorAll('.recipeImg');
    $.ajax({
        url: '/regen_images',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'title': recipeTitle , 'desc': recipeDesc, 'ingredients': recipeIngredients}),
        success: function(response) {
            for (let i = 0, len = imagesArray.length; i < len; i++) {
                imagesArray[i].src = response[i];
            };
        },
        error: function(error) {
            console.log(error);
        }
    });
}

const displaySubmitButton = document.querySelector("#displaySubmitbutton").addEventListener("click", submitRecipeForm);
const radioButtons = document.querySelectorAll('input[name="recipe_image"]');
    // Add a change event listener to each radio button
radioButtons.forEach(function(radioButton) {
    radioButton.addEventListener('change', function() {
        // Get the value (image source) of the selected radio button
        const selectedImageSrc = this.value;
    });
});
function submitRecipeForm () {
    const title = document.querySelector("#displayTitle").value;
    const description = document.querySelector("#displayDesc").value;
    const instructions = document.querySelector("#displayInstructions").value;
    const ingredients = document.querySelector("#displayIngredients").value;
    const recipeId = document.querySelector("#recipeId").value;
    const recipeImg = selectedImageSrc;
    console.log(title, description, instructions, ingredients, recipeId, recipeImg);
    $.ajax({
        url: "/save-recipe",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ 'title': title, 'description': description, 'instructions': instructions, 'ingredients': ingredients, 'id': recipeId, 'image_url': recipeImg}),
        success: function (response) {
            console.log("success");
        },
        error: function (error) {
            console.log(error);
        }
    });
};