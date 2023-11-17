const genButton = document.querySelector("#generateImage").addEventListener("click", generateImages);
function generateImages() {
    console.log('its getting new images');
    let prompt = document.querySelector("#image-prompt").value;
    let imagesDiv = document.querySelector("#images");
    console.log(prompt);
    console.log(imagesArray);
    $.ajax ({
        url: '/gen_images',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify( {'prompt': prompt}),
        success: function(response) {

            for (let i = 0, len = imagesArray.length; i < len; i++) {
                imagesArray[i].src = response[i];
            };
            },
            error: function(error) {
                console.log(error);
            }
    })
}