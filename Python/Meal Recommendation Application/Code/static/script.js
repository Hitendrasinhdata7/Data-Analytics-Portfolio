document.getElementById('user-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        name: formData.get('name'),
        age: formData.get('age'),
        height: formData.get('height'),
        weight: formData.get('weight'),
        category: formData.get('category')
    };

    fetch('/get-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(recommendations => {
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '<h2>Recommended Foods:</h2><ul>' + 
            recommendations.map(food => `<li>${food}</li>`).join('') + 
            '</ul>';
    });
});
