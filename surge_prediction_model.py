# surge_prediction_model.py
"""
Healthcare Surge Prediction Model using Random Forest
Predicts patient surge probability based on environmental, social, and health factors
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
import re
import json

class HealthcareSurgePredictionModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            min_samples_split=5,
            min_samples_leaf=2
        )
        self.scaler = StandardScaler()
        self.feature_columns = [
            'aqi_value', 'temperature', 'humidity', 'festival_score', 
            'baseline_admissions', 'hospital_occupancy', 'day_of_week',
            'month', 'respiratory_cases_trend', 'cardiac_cases_trend',
            'trauma_cases_trend', 'population_density'
        ]
        self.is_trained = False
        self.model_path = 'trained_surge_model.pkl'
        self.scaler_path = 'trained_scaler.pkl'
        
    def generate_synthetic_training_data(self, n_samples=5000):
        """
        Generate synthetic but realistic healthcare data for training
        Based on patterns from real healthcare surge research
        """
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Environmental factors
            aqi_value = np.random.normal(120, 40)  # Mumbai average AQI
            aqi_value = max(50, min(500, aqi_value))  # Clamp to realistic range
            
            temperature = np.random.normal(28, 5)  # Mumbai temperature in Celsius
            humidity = np.random.normal(75, 15)  # Mumbai humidity
            
            # Social factors
            is_festival = np.random.choice([0, 1], p=[0.85, 0.15])
            festival_score = is_festival * np.random.uniform(0.5, 1.0)
            
            # Hospital baseline
            baseline_admissions = np.random.normal(150, 30)  # Daily baseline
            baseline_admissions = max(80, baseline_admissions)
            
            hospital_occupancy = np.random.uniform(0.6, 0.95)
            
            # Time factors
            day_of_week = np.random.randint(0, 7)
            month = np.random.randint(1, 13)
            
            # Health trends (recent cases)
            respiratory_trend = np.random.normal(1.0, 0.3)  # Multiplier
            cardiac_trend = np.random.normal(1.0, 0.2)
            trauma_trend = np.random.normal(1.0, 0.25)
            
            population_density = np.random.normal(20000, 5000)  # People per sq km
            
            # Calculate surge probability based on realistic correlations
            surge_base = 0.1  # 10% base surge probability
            
            # AQI impact (higher AQI = more respiratory issues)
            if aqi_value > 200:
                surge_base += 0.3
            elif aqi_value > 150:
                surge_base += 0.15
            elif aqi_value > 100:
                surge_base += 0.05
            
            # Festival impact
            surge_base += festival_score * 0.25
            
            # Hospital occupancy impact (higher occupancy = more likely to see surge)
            if hospital_occupancy > 0.9:
                surge_base += 0.2
            elif hospital_occupancy > 0.8:
                surge_base += 0.1
            
            # Weekend effect (slightly higher)
            if day_of_week in [5, 6]:  # Saturday, Sunday
                surge_base += 0.05
            
            # Seasonal effects
            if month in [10, 11, 12, 1]:  # Winter months - more respiratory
                surge_base += respiratory_trend * 0.1
            
            # Health trend impacts
            surge_base += (respiratory_trend - 1) * 0.2
            surge_base += (cardiac_trend - 1) * 0.15
            surge_base += (trauma_trend - 1) * 0.1
            
            # Add some noise
            surge_base += np.random.normal(0, 0.05)
            
            # Clamp to reasonable range
            surge_probability = max(0.05, min(0.95, surge_base))
            
            # Convert to percentage increase in admissions
            surge_percentage = surge_probability * 60  # 0-60% increase range
            
            data.append({
                'aqi_value': aqi_value,
                'temperature': temperature,
                'humidity': humidity,
                'festival_score': festival_score,
                'baseline_admissions': baseline_admissions,
                'hospital_occupancy': hospital_occupancy,
                'day_of_week': day_of_week,
                'month': month,
                'respiratory_cases_trend': respiratory_trend,
                'cardiac_cases_trend': cardiac_trend,
                'trauma_cases_trend': trauma_trend,
                'population_density': population_density,
                'surge_percentage': surge_percentage,
                'surge_probability': surge_probability
            })
        
        return pd.DataFrame(data)
    
    def train_model(self, df=None):
        """Train the Random Forest model"""
        if df is None:
            print("Generating synthetic training data...")
            df = self.generate_synthetic_training_data()
        
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['surge_percentage']  # Predict percentage increase
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"  Mean Absolute Error: {mae:.2f}%")
        print(f"  R² Score: {r2:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop Feature Importances:")
        for _, row in feature_importance.head(5).iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        return mae, r2, feature_importance
    
    def save_model(self):
        """Save trained model and scaler"""
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load pre-trained model"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.is_trained = True
            print("Pre-trained model loaded successfully")
            return True
        return False
    
    def extract_features_from_text(self, data_summary: str):
        """
        Extract numerical features from the text data summary
        provided by the Data Fusion Agent
        """
        features = {}
        
        # Extract AQI value
        aqi_match = re.search(r'AQI\s*(\d+)', data_summary)
        features['aqi_value'] = float(aqi_match.group(1)) if aqi_match else 120
        
        # Extract temperature (if available)
        temp_match = re.search(r'temperature.*?(\d+)°?C?', data_summary, re.IGNORECASE)
        features['temperature'] = float(temp_match.group(1)) if temp_match else 28
        
        # Humidity (estimate based on location)
        features['humidity'] = 75  # Mumbai average
        
        # Festival score
        festival_keywords = ['festival', 'celebration', 'holiday', 'gathering']
        festival_score = sum(1 for keyword in festival_keywords if keyword.lower() in data_summary.lower())
        features['festival_score'] = min(festival_score / 4.0, 1.0)  # Normalize to 0-1
        
        # Extract hospital occupancy
        occupancy_match = re.search(r'occupancy.*?(\d+)%', data_summary, re.IGNORECASE)
        if occupancy_match:
            features['hospital_occupancy'] = float(occupancy_match.group(1)) / 100
        else:
            features['hospital_occupancy'] = 0.8  # Default
        
        # Extract baseline admissions (if mentioned)
        admission_match = re.search(r'(\d+)\s*beds?\s*occupied', data_summary, re.IGNORECASE)
        features['baseline_admissions'] = float(admission_match.group(1)) if admission_match else 150
        
        # Time-based features
        now = datetime.now()
        features['day_of_week'] = now.weekday()
        features['month'] = now.month
        
        # Health trends (analyze text for trend indicators)
        trend_indicators = {
            'respiratory_cases_trend': ['respiratory', 'breathing', 'asthma', 'pollution'],
            'cardiac_cases_trend': ['cardiac', 'heart', 'chest'],
            'trauma_cases_trend': ['trauma', 'injury', 'accident', 'festival']
        }
        
        for trend_type, keywords in trend_indicators.items():
            trend_score = 1.0  # Baseline
            
            if any(keyword in data_summary.lower() for keyword in keywords):
                if 'increase' in data_summary.lower():
                    trend_score = 1.3
                elif 'spike' in data_summary.lower() or 'surge' in data_summary.lower():
                    trend_score = 1.5
                elif 'decrease' in data_summary.lower():
                    trend_score = 0.8
            
            features[trend_type] = trend_score
        
        # Population density (Mumbai average)
        features['population_density'] = 20000
        
        return features
    
    def predict_surge(self, data_summary: str):
        """
        Main prediction function that takes text summary and returns detailed prediction
        """
        if not self.is_trained:
            if not self.load_model():
                # Train model if not available
                print("Training new model...")
                self.train_model()
        
        # Extract features from text
        features = self.extract_features_from_text(data_summary)
        
        # Create feature vector
        feature_vector = np.array([[features[col] for col in self.feature_columns]])
        
        # Scale features
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Make prediction
        predicted_surge_percentage = self.model.predict(feature_vector_scaled)[0]
        
        # Calculate confidence based on feature certainty
        confidence = self.calculate_confidence(features, data_summary)
        
        # Determine risk level
        if predicted_surge_percentage >= 40:
            risk_level = "Very High"
            timeline = "2-4 days"
        elif predicted_surge_percentage >= 25:
            risk_level = "High"
            timeline = "3-5 days"
        elif predicted_surge_percentage >= 15:
            risk_level = "Moderate"
            timeline = "5-7 days"
        else:
            risk_level = "Low"
            timeline = "7+ days"
        
        # Generate detailed prediction
        prediction_result = {
            'surge_percentage': max(0, predicted_surge_percentage),
            'confidence': confidence,
            'risk_level': risk_level,
            'timeline': timeline,
            'key_factors': self.identify_key_factors(features),
            'features_used': features
        }
        
        return prediction_result
    
    def calculate_confidence(self, features, data_summary):
        """Calculate prediction confidence based on data quality"""
        confidence = 70  # Base confidence
        
        # Boost confidence for specific data points
        if 'AQI' in data_summary and features['aqi_value'] != 120:
            confidence += 10  # Real AQI data
        
        if features['festival_score'] > 0:
            confidence += 8  # Festival data available
        
        if 'occupancy' in data_summary.lower():
            confidence += 7  # Hospital data available
        
        if any(trend != 1.0 for trend in [features['respiratory_cases_trend'], 
                                         features['cardiac_cases_trend'], 
                                         features['trauma_cases_trend']]):
            confidence += 5  # Health trend data
        
        return min(95, confidence)
    
    def identify_key_factors(self, features):
        """Identify the most significant risk factors"""
        factors = []
        
        if features['aqi_value'] > 150:
            factors.append(f"High air pollution (AQI: {features['aqi_value']:.0f})")
        
        if features['festival_score'] > 0.3:
            factors.append("Major festival/gathering period")
        
        if features['hospital_occupancy'] > 0.85:
            factors.append(f"High hospital occupancy ({features['hospital_occupancy']:.1%})")
        
        if features['respiratory_cases_trend'] > 1.2:
            factors.append("Increasing respiratory cases trend")
        
        if features['day_of_week'] in [5, 6]:
            factors.append("Weekend effect")
        
        return factors

# Initialize global model instance
surge_model = HealthcareSurgePredictionModel()

def initialize_model():
    """Initialize and train the model if needed"""
    if not surge_model.load_model():
        print("No pre-trained model found. Training new model...")
        surge_model.train_model()
    return surge_model

if __name__ == "__main__":
    # Test the model
    model = HealthcareSurgePredictionModel()
    mae, r2, importance = model.train_model()
    
    # Test prediction
    test_summary = """
    Real AQI Data for Mumbai: AQI 180 (Unhealthy). 
    Real Festival Data: Diwali celebrations in 3 days.
    Hospital occupancy: 87% occupied.
    Minor increase in respiratory illnesses reported.
    """
    
    result = model.predict_surge(test_summary)
    print(f"\nTest Prediction:")
    print(f"Surge Percentage: {result['surge_percentage']:.1f}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Key Factors: {', '.join(result['key_factors'])}")
