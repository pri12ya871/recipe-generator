document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript loaded');  // Add this line
    document.getElementById('uploadForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('image', document.getElementById('image').files[0]);

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();
            console.log(data);  // For debugging

            document.getElementById('className').textContent = `Class: ${data.predicted_class}`;

            const ingredients = data.recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('');
            const steps = data.recipe.steps.map(step => `<li>${step}</li>`).join('');

            document.getElementById('recipeIngredients').innerHTML = ingredients;
            document.getElementById('recipeSteps').innerHTML = steps;

        } catch (error) {
            console.error('Error:', error);
            document.getElementById('className').textContent = 'Error occurred during classification.';
        }
    });
});
