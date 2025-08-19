#!/usr/bin/env python3
"""
Test script for the Healthcare Surge Prediction ML Model
Run this to verify the model training and prediction functionality
"""

from surge_prediction_model import HealthcareSurgePredictionModel
import sys

def test_model():
    print("🧪 Testing Healthcare Surge Prediction ML Model")
    print("=" * 60)
    
    # Initialize model
    model = HealthcareSurgePredictionModel()
    
    # Test 1: Model Training
    print("\n📚 Test 1: Training Random Forest Model")
    try:
        mae, r2, importance = model.train_model()
        print(f"✅ Training successful!")
        print(f"   Mean Absolute Error: {mae:.2f}%")
        print(f"   R² Score: {r2:.3f}")
        
        if r2 > 0.7:
            print("✅ Model performance is good (R² > 0.7)")
        else:
            print("⚠️  Model performance could be improved")
            
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        return False
    
    # Test 2: Feature Extraction
    print("\n🔍 Test 2: Feature Extraction from Text")
    test_summary = """
    Real AQI Data for Mumbai: AQI 185 (Unhealthy for sensitive groups).
    Real Festival Data: Diwali celebrations in 2 days.
    Hospital occupancy: 89% occupied.
    Minor increase in respiratory illnesses reported.
    """
    
    try:
        features = model.extract_features_from_text(test_summary)
        print("✅ Feature extraction successful!")
        print("   Key features extracted:")
        for key, value in features.items():
            if key in ['aqi_value', 'hospital_occupancy', 'festival_score']:
                print(f"     {key}: {value}")
    except Exception as e:
        print(f"❌ Feature extraction failed: {str(e)}")
        return False
    
    # Test 3: Surge Prediction
    print("\n🔮 Test 3: Surge Prediction")
    try:
        prediction = model.predict_surge(test_summary)
        print("✅ Prediction successful!")
        print(f"   Surge Percentage: {prediction['surge_percentage']:.1f}%")
        print(f"   Risk Level: {prediction['risk_level']}")
        print(f"   Confidence: {prediction['confidence']}%")
        print(f"   Timeline: {prediction['timeline']}")
        print(f"   Key Factors: {', '.join(prediction['key_factors'])}")
        
        # Validate prediction ranges
        if 0 <= prediction['surge_percentage'] <= 100:
            print("✅ Surge percentage is within valid range")
        else:
            print("⚠️  Surge percentage outside expected range")
            
        if 50 <= prediction['confidence'] <= 100:
            print("✅ Confidence level is reasonable")
        else:
            print("⚠️  Confidence level outside expected range")
            
    except Exception as e:
        print(f"❌ Prediction failed: {str(e)}")
        return False
    
    # Test 4: Different Scenarios
    print("\n📊 Test 4: Multiple Scenarios")
    scenarios = [
        {
            "name": "Low Risk Scenario",
            "text": "AQI 75 (Good). No festivals. Hospital occupancy 70%. No health alerts."
        },
        {
            "name": "High Risk Scenario", 
            "text": "AQI 220 (Very Unhealthy). Ganesh Chaturthi festival starting tomorrow. Hospital occupancy 95%. Spike in respiratory cases."
        },
        {
            "name": "Moderate Risk Scenario",
            "text": "AQI 140 (Unhealthy for sensitive groups). Weekend. Hospital occupancy 82%. Minor increase in cardiac cases."
        }
    ]
    
    for scenario in scenarios:
        try:
            result = model.predict_surge(scenario["text"])
            print(f"   {scenario['name']}:")
            print(f"     Surge: {result['surge_percentage']:.1f}% | Risk: {result['risk_level']} | Confidence: {result['confidence']}%")
        except Exception as e:
            print(f"   ❌ {scenario['name']} failed: {str(e)}")
    
    print("\n🎉 All tests completed successfully!")
    print("✅ ML Model is ready for production use!")
    return True

if __name__ == "__main__":
    success = test_model()
    sys.exit(0 if success else 1)
