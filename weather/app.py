import os
import requests
from flask import Flask, render_template, request, flash
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# WeatherAPI.com configuration
API_KEY = os.getenv('WEATHERAPI_KEY')
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

def get_demo_weather_data():
    """Return demo weather data for testing without API key"""
    from datetime import datetime, timedelta
    
    demo_data = []
    base_date = datetime.now().date()
    
    # Create 3 days of demo data with different conditions
    conditions = [
        {'temp': 28, 'humidity': 85, 'rain': 12, 'desc': 'Heavy Rain'},
        {'temp': 32, 'humidity': 45, 'rain': 0, 'desc': 'Sunny'},
        {'temp': 25, 'humidity': 75, 'rain': 3, 'desc': 'Partly Cloudy'}
    ]
    
    for i, condition in enumerate(conditions):
        date = base_date + timedelta(days=i+1)
        demo_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'day_name': date.strftime('%A'),
            'temp': condition['temp'],
            'humidity': condition['humidity'],
            'description': condition['desc'],
            'rain': condition['rain']
        })
    
    return demo_data

def get_weather_forecast(location):
    """Fetch 3-day weather forecast for the given location"""
    try:
        # Demo mode if no API key is configured
        if not API_KEY or API_KEY == 'your-weatherapi-key-here':
            return get_demo_weather_data()
        
        params = {
            'key': API_KEY,
            'q': location,
            'days': 3,
            'aqi': 'no',
            'alerts': 'no'
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process forecast data for next 3 days
        forecast_data = []
        
        for day in data['forecast']['forecastday']:
            forecast_data.append({
                'date': day['date'],
                'day_name': datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A'),
                'temp': round(day['day']['avgtemp_c']),
                'humidity': day['day']['avghumidity'],
                'description': day['day']['condition']['text'],
                'rain': day['day']['totalprecip_mm']
            })
        
        return forecast_data
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def analyze_disease_risk(forecast_data):
    """Analyze weather conditions and predict disease risks"""
    diseases = []
    
    for day in forecast_data:
        temp = day['temp']
        humidity = day['humidity']
        rain = day['rain']
        
        day_diseases = []
        
        # High fungal risk: humidity > 80% and temp 20-30°C
        if humidity > 80 and 20 <= temp <= 30:
            day_diseases.append({
                'name': 'Powdery Mildew',
                'risk': 'High',
                'description': 'Fungal disease affecting leaves and stems'
            })
            day_diseases.append({
                'name': 'Leaf Spot',
                'risk': 'High',
                'description': 'Dark spots on leaves caused by fungi'
            })
        
        # Mites/Leaf Curl risk: temp > 32°C and dry
        if temp > 32 and humidity < 50:
            day_diseases.append({
                'name': 'Mites Infestation',
                'risk': 'High',
                'description': 'Tiny pests causing leaf damage'
            })
            day_diseases.append({
                'name': 'Leaf Curl',
                'risk': 'Medium',
                'description': 'Leaves curling due to heat stress'
            })
        
        # Blight/Root Rot risk: continuous rain
        if rain > 5:  # More than 5mm rain
            day_diseases.append({
                'name': 'Blight',
                'risk': 'High',
                'description': 'Rapid plant death due to excessive moisture'
            })
            day_diseases.append({
                'name': 'Root Rot',
                'risk': 'High',
                'description': 'Root system damage from waterlogging'
            })
        
        # Additional conditions
        if humidity > 90:
            day_diseases.append({
                'name': 'Anthracnose',
                'risk': 'Medium',
                'description': 'Fungal disease in high humidity'
            })
        
        if temp < 10:
            day_diseases.append({
                'name': 'Frost Damage',
                'risk': 'High',
                'description': 'Cold damage to plant tissues'
            })
        
        diseases.append({
            'date': day['date'],
            'day_name': day['day_name'],
            'conditions': day_diseases
        })
    
    return diseases

def get_precautions():
    """Return list of general precautions for farmers"""
    return [
        {
            'category': 'Preventive Measures',
            'tips': [
                'Ensure proper spacing between plants for air circulation',
                'Water plants at the base, avoid wetting leaves',
                'Remove and destroy infected plant debris',
                'Rotate crops annually to prevent soil-borne diseases'
            ]
        },
        {
            'category': 'Eco-friendly Remedies',
            'tips': [
                'Spray neem oil solution (2ml per liter water) weekly',
                'Use baking soda spray (1 tsp per liter water) for fungal issues',
                'Apply garlic and chili pepper spray for pest control',
                'Use compost tea as a natural fertilizer and disease suppressant'
            ]
        },
        {
            'category': 'Drainage & Soil Health',
            'tips': [
                'Improve soil drainage with organic matter',
                'Avoid overwatering, especially in humid conditions',
                'Use raised beds in areas with poor drainage',
                'Test soil pH and maintain optimal levels (6.0-7.0)'
            ]
        },
        {
            'category': 'Monitoring & Early Detection',
            'tips': [
                'Inspect plants regularly for early signs of disease',
                'Keep a garden journal to track weather and plant health',
                'Remove weeds that can harbor disease-causing organisms',
                'Quarantine new plants before introducing to your garden'
            ]
        }
    ]

@app.route('/')
def home():
    """Homepage with location input form"""
    return render_template('index.html')

@app.route('/check_risk', methods=['POST'])
def check_risk():
    """Process form submission and analyze disease risk"""
    location = request.form.get('location', '').strip()
    
    if not location:
        flash('Please enter a location', 'error')
        return render_template('index.html')
    
    if not API_KEY or API_KEY == 'your-weatherapi-key-here':
        flash('WeatherAPI key not configured. Using demo data for testing. Get your free API key from https://www.weatherapi.com/my/', 'warning')
        # Continue with demo data instead of returning
    
    # Get weather forecast
    forecast_data = get_weather_forecast(location)
    
    if not forecast_data:
        flash('Unable to fetch weather data. Please check the location name and try again.', 'error')
        return render_template('index.html')
    
    # Analyze disease risks
    disease_analysis = analyze_disease_risk(forecast_data)
    
    # Get precautions
    precautions = get_precautions()
    
    return render_template('results.html', 
                         location=location,
                         forecast=forecast_data,
                         diseases=disease_analysis,
                         precautions=precautions)

if __name__ == '__main__':
    app.run(debug=True)
