function triggerRegen() {
    const recipeTitle = document.getElementById('recipe_title').innerText;
    const recipeDesc = document.getElementById('recipe_desc').innerText;
    fetch('/regen_images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: recipeTitle,
            description: recipeDesc,
            instructions: '{{ instructions | tojson }}',
            ingredients_list: '{{ ingredients_list | tojson }}'
        })
    })
        .then(response => {
            if (response.ok) {
                console.log('Image regeneration started.');
                return response.json();
            } else {
                console.log('Error triggering image regeneration.');
                throw new Error('Error triggering image regeneration.');
            }
        })
        .then(data => {
            const imageContainer = document.getElementById('imageContainer');
            imageContainer.innerHTML = '';
            data.images.forEach(imageUrl => {
                const buttonElement = document.createElement('button');
                const imgElement = document.createElement('img');
                imgElement.src = imageUrl;
                imgElement.alt = 'Recipe Image';
                buttonElement.appendChild(imgElement);
                imageContainer.appendChild(buttonElement);
            });
        })
        .catch(error => console.error(error));
}

// <script src="{{ url_for('static', filename='script.js') }}"></script>
// This ^^ goes in the header and at the botttom of the <body>
// I need to learn how to pass the appropriate values to the JS file.