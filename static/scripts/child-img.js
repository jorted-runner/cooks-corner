const genButton = document.querySelector("#generateImage").addEventListener("click", generateImages);
function generateImages() {
    console.log('its getting new images');
    let prompt = document.querySelector("#image-prompt").value;
    let imagesContainer = document.querySelector("#images");
    console.log(prompt);
    $.ajax ({
        url: '/gen_images',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify( {'prompt': prompt}),
        success: function(response) {
            console.log("it succeded in getting images back to the JS file.");
            for (let i = 0; i < 2; i++) {
                var imageDiv = document.createElement('div');
                imageDiv.setAttribute("id", `image-${i}`);

                var imageRadio = document.createElement('input');
                imageRadio.setAttribute('type', 'radio');
                imageRadio.setAttribute('id', `image_${i}`);
                imageRadio.setAttribute('name', 'child_image');
                imageDiv.appendChild(imageRadio);

                var imageLabel = document.createElement('label');
                imageLabel.setAttribute('for', `image_${i}`);

                var imageElement = document.createElement('img')
                imageElement.setAttribute('src', response[i]);
                imageElement.setAttribute('class', 'childImages');
                imageElement.setAttribute('alt', 'Childrens Book Generated Image');

                imageLabel.appendChild(imageElement);

                imageDiv.appendChild(imageLabel);
                imagesContainer.appendChild(imageDiv);
            };
        }, 
        error: function(error) {
            console.log(error);
        }
    });
}

const SaveImage = document.querySelector("#saveImageButton").addEventListener("click", saveGeneratedImage);
function saveGeneratedImage(event) {
    event.preventDefault();
    var fileName = document.querySelector('input[name="filename"]').value;
    const radioButtons = document.querySelectorAll('input[name="child_image"]');
    let selectedImageSrc;
    radioButtons.forEach(function (radioButton) {
        if (radioButton.checked) {
            const imageId = radioButton.id.split("_")[1];
            selectedImageSrc = document.querySelector(`#image-${imageId} img`).src;
        }
    });
    
    const selectedImage = selectedImageSrc;
    $.ajax({
        url: "/save-childrens-book-image",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ 'image_url': selectedImage, 'fileName': fileName }),
        success: function (response) {
            console.log("success");
            window.location.href = "/childrens-book";
        },
        error: function (error) {
            console.log(error);
        }
    });
}