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