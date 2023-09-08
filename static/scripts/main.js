let cardArray = document.querySelectorAll('.card__inner');

cardArray.forEach(function(elem) {
    elem.addEventListener('click', function() {
        elem.classList.toggle('is-flipped');
    });
});

function confirmDelete(recipeId) {
    Swal.fire({
      title: 'Confirm Deletion',
      text: 'Are you sure you want to delete this recipe from Cooks Corner?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it',
      cancelButtonText: 'No, cancel',
    }).then((result) => {
      if (result.isConfirmed) {
      } else {
      }
    }).then(() => {
      const form = document.querySelector(`#delete-form-${recipeId}`);
      form.submit();
    }).catch(error => {
      console.error(error);
    });
  }
  
    