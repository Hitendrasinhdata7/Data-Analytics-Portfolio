from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Load the CSV file
try:
    food_data = pd.read_csv(r'C:\Users\HP\Desktop\Bapu\FlaskF\Food_with_Category.csv')
    food_data.columns = food_data.columns.str.strip()  # Strip any extra spaces from column names
except FileNotFoundError:
    raise Exception("CSV file not found. Please check the file path.")

# Static mapping from dataset categories to form categories
category_mapping = {
    'gym_enthusiast': [
        'CannedFruit', 'Fruits', 'Tropical&ExoticFruits', 'PotatoProducts',
        'Vegetables', 'Milk&DairyProducts', 'SlicedCheese', 'Yogurt',
        'Beef&Veal', 'ColdCuts&LunchMeat', 'Meat', 'Pork', 'Poultry&Fowl',
        'Venison&Game', 'Legumes', 'Nuts&Seeds', 'Fish&Seafood'
    ],
    'sportsman': [
        'Pizza', 'Cheese', 'CreamCheese', 'Offal&Giblets', 'Sausage',
        'Cakes&Pies', 'Candy&Sweets', 'IceCream', '(Fruit)Juices',
        'CerealProducts', 'Oatmeal,Muesli&Cereals', 'Pasta&Noodles',
        'Dishes&Meals', 'Soups', 'Oils&Fats', 'VegetableOils'
    ],
    'specific_conditions': [
        'AlcoholicDrinks&Beverages', 'Beer', 'Non-AlcoholicDrinks&Beverages',
        'Soda&SoftDrinks', 'Wine', 'BakingIngredients', 'Herbs&Spices',
        'Pastries,Breads&Rolls', 'Sauces&Dressings', 'Spreads'
    ]
}

# Reverse mapping from dataset category to form category
dataset_to_form_mapping = {}
for form_category, dataset_categories in category_mapping.items():
    for dataset_category in dataset_categories:
        dataset_to_form_mapping[dataset_category] = form_category

# Diet preference mapping
diet_preference_mapping = {
    'CannedFruit': 'veg',
    'Fruits': 'veg',
    'Tropical&ExoticFruits': 'veg',
    'PotatoProducts': 'veg',
    'Vegetables': 'veg',
    'Milk&DairyProducts': 'veg',
    'SlicedCheese': 'veg',
    'Yogurt': 'veg',
    'Beef&Veal': 'non-veg',
    'ColdCuts&LunchMeat': 'non-veg',
    'Meat': 'non-veg',
    'Pork': 'non-veg',
    'Poultry&Fowl': 'non-veg',
    'Venison&Game': 'non-veg',
    'Fish&Seafood': 'non-veg'
}

# Clustering configuration
num_clusters = 5  # Define the number of clusters

# Preprocessing the data
def preprocess_data(data):
    features = data[['calories']]  # You can include more features if available
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    return scaled_features

# Fit the KMeans model
def fit_kmeans_model(data):
    scaled_data = preprocess_data(data)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(scaled_data)
    data['Cluster'] = kmeans.labels_
    return data, kmeans

# Fit the model once at the start
food_data, kmeans_model = fit_kmeans_model(food_data)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/view-dataset')
def view_dataset_analysis():
    return render_template('view_dataset_Analysis.html')

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    name = request.form['name']
    age = int(request.form['age'])
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    form_category = request.form['category']
    diet_preference = request.form['diet_preference']
    num_suggestions = int(request.form['num_suggestions'])

    # Debug: Log the selected form category and diet preference
    print(f"Selected Form Category: {form_category}")
    print(f"Selected Diet Preference: {diet_preference}")

    relevant_categories = [cat for cat, mapped_cat in dataset_to_form_mapping.items() if mapped_cat == form_category]

    # Debug: Log the relevant categories
    print(f"Relevant Categories: {relevant_categories}")

    if not relevant_categories:
        return render_template('index.html', name=name, recommendations=['No relevant categories found for the selected form category.'])

    filtered_food_data = food_data[
        (food_data['FoodCategory'].isin(relevant_categories))
    ]

    # Debug: Check if filtered_food_data is empty
    if filtered_food_data.empty:
        print("No foods found for the selected categories.")
        return render_template('index.html', name=name, recommendations=['No foods found for the selected categories.'])

    # Filter based on diet preference using diet_preference_mapping
    filtered_food_data['DietPreference'] = filtered_food_data['FoodCategory'].map(diet_preference_mapping)
    filtered_food_data = filtered_food_data[
        filtered_food_data['DietPreference'] == diet_preference
    ]

    # Debug: Check if filtered_food_data is empty after diet preference filtering
    if filtered_food_data.empty:
        print("No foods found for the selected categories and diet preference.")
        return render_template('index.html', name=name, recommendations=['No foods found for the selected categories and diet preference.'])

    # Add clustering-based recommendations
    user_preference_cluster = filtered_food_data.iloc[0]['Cluster'] if not filtered_food_data.empty else None
    if user_preference_cluster is not None:
        cluster_recommendations = food_data[food_data['Cluster'] == user_preference_cluster]
        cluster_recommendations = cluster_recommendations.sort_values(by='calories', ascending=False).head(num_suggestions)
    else:
        cluster_recommendations = filtered_food_data.sort_values(by='calories', ascending=False).head(num_suggestions)

    # Debug: Check if cluster_recommendations is empty
    if cluster_recommendations.empty:
        print("No cluster-based recommendations found.")
        return render_template('index.html', name=name, recommendations=['No cluster-based recommendations found.'])

    recommended_foods = cluster_recommendations[['FoodItem', 'calories']].values.tolist()
    total_calories = cluster_recommendations['calories'].sum()

    return render_template('index.html', name=name, age=age, height=height, weight=weight,
                           category=form_category, diet_preference=diet_preference,
                           num_suggestions=num_suggestions,
                           recommendations=recommended_foods, total_calories=total_calories)


if __name__ == '__main__':
    app.run(debug=True)
