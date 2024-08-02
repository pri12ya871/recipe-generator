from flask import Blueprint, request, jsonify, render_template
from transformers import pipeline, AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import json
import os

main = Blueprint('main', __name__)

# Initialize the model and feature extractor
repo_name = "rajistics/finetuned-indian-food"
feature_extractor = AutoImageProcessor.from_pretrained(repo_name)
model = AutoModelForImageClassification.from_pretrained(repo_name)
pipe = pipeline("image-classification", model=model, feature_extractor=feature_extractor)

# Load recipes from JSON file
recipes_path = os.path.join(os.path.dirname(__file__), 'recipes.json')
if not os.path.isfile(recipes_path):
    raise FileNotFoundError(f"Recipes file not found: {recipes_path}")

with open(recipes_path, 'r') as f:
    recipes = json.load(f)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    try:
        image = Image.open(file.stream).convert("RGB")  # Ensure image is in RGB format
    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 400
    
    # Using the pipeline for classification
    try:
        classification_result = pipe(image)
    except Exception as e:
        return jsonify({"error": f"Error during classification: {str(e)}"}), 500
    
    # Get the predicted class
    predicted_class = classification_result[0]['label']
    print(f"Predicted class: {predicted_class}")  # Print class to console
    
    # Get the recipe for the predicted class
    recipe = recipes.get(predicted_class, {"ingredients": [], "steps": []})
    
    return jsonify({
        "predicted_class": predicted_class,
        "recipe": recipe
    })
