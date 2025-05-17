from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data for training (in a real app, you'd use a proper dataset)
sample_data = {
    'location': ['urban', 'suburban', 'rural', 'urban', 'suburban', 'rural'],
    'bedrooms': [3, 2, 4, 2, 3, 1],
    'bathrooms': [2, 1.5, 2.5, 1, 2, 1],
    'sqft': [1500, 1200, 2000, 1000, 1400, 800],
    'year': [2010, 1995, 2005, 1980, 2015, 1975],
    'condition': ['good', 'average', 'excellent', 'fair', 'good', 'poor'],
    'price': [350000, 275000, 450000, 200000, 320000, 150000]
}

# Convert to DataFrame
df = pd.DataFrame(sample_data)

# Preprocess the data
def preprocess_data(df):
    # Convert categorical variables to numerical
    df['location'] = df['location'].map({'urban': 2, 'suburban': 1, 'rural': 0})
    df['condition'] = df['condition'].map({'excellent': 4, 'good': 3, 'average': 2, 'fair': 1, 'poor': 0})
    return df

# Train or load the model
def get_model():
    model_path = 'house_price_model.pkl'
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        # Prepare data
        processed_df = preprocess_data(df.copy())
        X = processed_df.drop('price', axis=1)
        y = processed_df['price']
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, model_path)
        return model

model = get_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        
        # Create input DataFrame
        input_data = pd.DataFrame([{
            'location': data['location'],
            'bedrooms': int(data['bedrooms']),
            'bathrooms': float(data['bathrooms']),
            'sqft': int(data['sqft']),
            'year': int(data['year']),
            'condition': data['condition']
        }])
        
        # Preprocess
        processed_input = preprocess_data(input_data)
        
        # Predict
        prediction = model.predict(processed_input)
        
        # Return prediction
        return jsonify({
            'predicted_price': int(prediction[0]),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/')
def home():
    return "House Price Prediction API is running!"

if __name__ == '__main__':
    app.run(debug=True)