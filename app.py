from flask import Flask, render_template, request, send_from_directory, redirect, url_for, abort, g, jsonify
import os
import sqlite3
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests

# If hydro_utils is available, import it
try:
    from hydro.hydro_utils import recommend_system, nutrient_recipe
except ImportError:
    recommend_system = None
    nutrient_recipe = None

app = Flask(__name__, template_folder='templates', static_folder='static')
load_dotenv()

# --- AI Crop Disease (from crop1/crop/app.py) ---
DATABASE = os.path.join(os.path.dirname(__file__), 'crop1', 'crop', 'community.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'crop1', 'crop', 'uploads')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'crop1', 'crop', 'model', 'plant_disease_model.h5')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
model = load_model(MODEL_PATH, compile=False)
class_names = ['Tomato-Bacterial_spot', 'Potato-Barly blight', 'Corn-Common_rust']
remedies = {
    'Tomato-Bacterial_spot': {
        "Treatment": ["Remove infected leaves.", "Spray copper-based fungicide every 7-10 days.", "Neem oil can be used as an organic alternative."],
        "Prevention": ["Use disease-free seeds.", "Maintain proper spacing between plants.", "Rotate crops yearly."],
        "Fertilizer Advice": ["Apply Nitrogen 20kg/acre + Potassium 10kg/acre.", "Neem-based organic fertilizer optional."],
        "Watering Tips": ["Avoid overhead irrigation.", "Water early morning."],
        "Harvest Advice": ["Harvest promptly to avoid contact with infected foliage.", "Discard severely infected fruits."],
        "Extra Tips": ["Monitor plants regularly.", "Maintain good ventilation in greenhouses."]
    },
    'Potato-Barly blight': {
        "Treatment": ["Apply fungicides like mancozeb or chlorothalonil.", "Remove severely affected plants."],
        "Prevention": ["Plant resistant varieties.", "Practice crop rotation.", "Space plants adequately."],
        "Fertilizer Advice": ["Use balanced NPK fertilizer: N15:P15:K15.", "Compost can improve soil health."],
        "Watering Tips": ["Irrigate in the morning.", "Avoid waterlogging."],
        "Harvest Advice": ["Harvest when foliage is dry.", "Store in cool, dry conditions."],
        "Extra Tips": ["Destroy volunteer plants.", "Monitor brown lesions on leaves."]
    },
    'Corn-Common_rust': {
        "Treatment": ["Remove heavily infected plants.", "Apply azoxystrobin fungicide.", "Sulfur sprays for organic control."],
        "Prevention": ["Plant resistant hybrids.", "Rotate crops.", "Maintain field sanitation."],
        "Fertilizer Advice": ["Apply NPK 16:16:16 as basal dose.", "Top-dress with Nitrogen mid-growth."],
        "Watering Tips": ["Avoid late evening irrigation.", "Reduce leaf wetness."],
        "Harvest Advice": ["Harvest when kernels are fully mature.", "Remove debris post-harvest."],
        "Extra Tips": ["Inspect lower leaves regularly.", "Improve airflow between plants.", "Avoid overcrowding."]
    }
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        );
        ''')
        db.commit()
init_db()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/ai-disease", methods=["GET", "POST"])
def ai_disease():
    disease = None
    remedy_info = None
    filename = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename != "":
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            img = Image.open(filepath).convert('RGB').resize((256, 256))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            Y_pred = model.predict(img_array)
            predicted_index = np.argmax(Y_pred)
            confidence = np.max(Y_pred)
            if confidence < 0.6:
                disease = "Unable to detect"
                remedy_info = {
                    "Treatment": "Please upload a clear image.",
                    "Prevention": "Ensure proper lighting and focus.",
                    "Tips": "Make sure the leaf is centered and healthy."
                }
            else:
                disease = class_names[predicted_index]
                remedy_info = remedies[disease]
    return render_template("crop_templates/index.html", 
                       disease=disease, 
                       remedy=remedy_info, 
                       result=bool(disease), 
                       filename=filename)
@app.route('/community')
def community():
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    return render_template('crop_templates/community.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        disease = request.form['disease']
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        db.execute('INSERT INTO posts (disease, title, content) VALUES (?, ?, ?)', (disease, title, content))
        db.commit()
        return redirect(url_for('community'))
    return render_template('crop_templates/new_post.html')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if not post:
        return "Post not found", 404
    if request.method == 'POST':
        comment = request.form['comment']
        if comment:
            db.execute('INSERT INTO comments (post_id, content) VALUES (?, ?)', (post_id, comment))
            db.commit()
    comments = db.execute('SELECT content FROM comments WHERE post_id = ? ORDER BY id ASC', (post_id,)).fetchall()
    return render_template('post_detail.html', post=post, comments=comments)

# --- Food Security/NGO/Markets (from FarmConnect/app.py) ---
submissions = []
NGO_DATA = {
    "save-the-humanity": {
        "slug": "save-the-humanity",
        "name": "Save The Humanity Foundation",
        "image": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&q=80&auto=format&fit=crop",
        "short": "Working on hunger relief and food security through meal distribution.",
        "description": "Save The Humanity Foundation focuses on providing nutritious meals to underprivileged communities and supporting food security initiatives across India.",
        "stats": {
            "meals_distributed": 500000,
            "communities_served": 150,
            "volunteers": 1200
        },
        "needs": "Raw materials for meal preparation, cooking equipment, and transportation support.",
        "website": "https://www.savethehumanity.org.in/",
        "donate_url": "https://www.savethehumanity.org.in/raw-material-meal-distribution/"
    },
    "akshaya-patra": {
        "slug": "akshaya-patra",
        "name": "Akshaya Patra Foundation",
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=80&auto=format&fit=crop",
        "short": "Working on hunger relief and food security through school meal programs.",
        "description": "Akshaya Patra Foundation runs the world's largest NGO-run school lunch program, serving millions of children daily across India.",
        "stats": {
            "children_served": 1800000,
            "schools": 19000,
            "meals_per_day": 1800000
        },
        "needs": "Grocery kits, dry rations, and kitchen equipment for meal preparation.",
        "website": "https://www.akshayapatra.org/",
        "donate_url": "https://www.akshayapatra.org/photo-gallery/grocery-kit-distribution-during-2nd-wave-of-covid"
    },
    "aapke-saath": {
        "slug": "aapke-saath",
        "name": "Aapke Saath Foundation",
        "image": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800&q=80&auto=format&fit=crop",
        "short": "Working on hunger relief and food security through dry ration distribution.",
        "description": "Aapke Saath Foundation provides monthly dry ration kits to families in need, ensuring food security for vulnerable communities.",
        "stats": {
            "families_served": 25000,
            "ration_kits_distributed": 300000,
            "cities_covered": 25
        },
        "needs": "Dry rations, rice, wheat, pulses, and essential food items.",
        "website": "https://asf.org.in/",
        "donate_url": "https://asf.org.in/monthly-dry-ration-kit-distribution-campaign-drive/"
    },
    "india-foodbanking": {
        "slug": "india-foodbanking",
        "name": "India FoodBanking Network",
        "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800&q=80&auto=format&fit=crop",
        "short": "Working on hunger relief and food security through food banking network.",
        "description": "India FoodBanking Network creates a sustainable food banking ecosystem to reduce hunger and food waste across India.",
        "stats": {
            "food_banks": 45,
            "meals_distributed": 2000000,
            "partner_ngos": 200
        },
        "needs": "Food donations, cold storage facilities, and logistics support.",
        "website": "https://www.indiafoodbanking.org/",
        "donate_url": "https://www.indiafoodbanking.org/foodbanking/"
    }
} # Use the full dict from FarmConnect/app.py
MARKETS_DATA = [
    {
        "market_name": "Bangalore Market",
        "location": "Bangalore",
        "produce": "Tomatoes",
        "quantity": "5 KG",
        "contact_primary": "+91 98748 23458",
        "contact_full": "+91 98748 23458, buyer@bangalore-market.com",
    },
    {
        "market_name": "FreshHub Market",
        "location": "Mumbai",
        "produce": "Potatoes",
        "quantity": "2 KG",
        "contact_primary": "+91 93245 67890",
        "contact_full": "+91 93245 67890, orders@mumbai-market.com",
    },
    {
        "market_name": "GreenCart Aggregators",
        "location": "Chennai",
        "produce": "Onions",
        "quantity": "800 KG",
        "contact_primary": "+91 99876 54321",
        "contact_full": "+91 99876 54321, procurement@chennai-market.com",
    },
    {
        "market_name": "MarketLink Traders",
        "location": "Delhi",
        "produce": "Bananas",
        "quantity": "120 KG",
        "contact_primary": "+91 98765 43210",
        "contact_full": "+91 98765 43210, trade@delhi-market.com",
    },
    {
        "market_name": "AgroServe Mart",
        "location": "Kolkata",
        "produce": "Mangoes",
        "quantity": "600 KG",
        "contact_primary": "+91 93987 65432",
        "contact_full": "+91 93987 65432, mango@kolkata-market.com",
    },
] # Use the full list from FarmConnect/app.py

@app.route("/food-security")
def food_security_home():
    return render_template("farmconnect_templates/index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    success_message = None
    if request.method == "POST":
        farmer_name = request.form.get("farmer_name", "").strip()
        contact = request.form.get("contact", "").strip()
        produce_name = request.form.get("produce_name", "").strip()
        quantity_value = request.form.get("quantity_value", "").strip()
        quantity_unit = request.form.get("quantity_unit", "kg").strip()
        location = request.form.get("location", "").strip()
        if farmer_name and contact and produce_name and quantity_value and location:
            submissions.append({
                "farmer_name": farmer_name,
                "contact": contact,
                "produce_name": produce_name,
                "quantity": f"{quantity_value} {quantity_unit}",
                "location": location,
            })
            success_message = "Submission received successfully."
    return render_template("farmconnect_templates/upload.html", success_message=success_message, submissions=submissions)

@app.route("/markets")
def markets():
    return render_template("farmconnect_templates/markets.html", markets=MARKETS_DATA)

@app.route("/ngos")
def ngos():
    ngos_list = list(NGO_DATA.values())
    return render_template("farmconnect_templates/ngos.html", ngos=ngos_list)

@app.route("/ngos/<slug>")
def ngo_detail(slug: str):
    ngo = NGO_DATA.get(slug)
    if not ngo:
        abort(404)
    return render_template("farmconnect_templates/ngo_detail.html", ngo=ngo)

# --- Hydroponics (from hydro/app.py) ---
@app.route("/hydro")
def hydro_home():
    return render_template("hydro_templates/hydro_info.html", title="Hydroponics Info")

@app.route("/hydro/recommend", methods=["GET", "POST"])
def hydro_recommend():
    result = None
    if request.method == "POST" and recommend_system:
        crop = request.form.get("crop", "").strip()
        space = request.form.get("space", "").strip()
        budget = request.form.get("budget", "").strip()
        lighting = request.form.get("lighting", "").strip()
        result = recommend_system(crop, space, budget, lighting)
    return render_template("hydro_templates/hydro_recommend.html", title="Recommendation Tool", result=result)

@app.route("/hydro/nutrients", methods=["GET", "POST"])
def hydro_nutrients():
    mix = None
    if request.method == "POST" and nutrient_recipe:
        crop = request.form.get("crop", "").strip()
        mix = nutrient_recipe(crop)
    return render_template("hydro_templates/hydro_nutrients.html", title="Nutrient Mix", mix=mix)

@app.route("/hydro/setup")
def hydro_setup_page():
    return render_template("hydro_templates/hydro_setup.html", title="Hydroponics Setup & Materials")

@app.route("/gobar-gas")
def gobar_gas():
    return render_template("gobar_index.html")

@app.route("/")
def home():
    return render_template("main-home.html")

@app.route("/weather", methods=["GET", "POST"])
def weather_home():
    if request.method == "POST":
        location = request.form.get("location", "").strip()
        if location:
            # Store location in session or pass it properly
            return weather_results_with_location(location)
        else:
            error = "Please enter a city name."
            return render_template("weather_templates/index.html", error=error)
    
    return render_template("weather_templates/index.html")

def weather_results_with_location(location):
    # Your existing weather_results logic here, but accept location as parameter
    # ... (use the code I provided earlier)
    pass

@app.route("/results", methods=["POST"])
def weather_results():
    location = request.form["location"]
    forecast = []
    diseases = []
    precautions = []
    error = None

    # Fetch weather data from WeatherAPI
    api_key = os.environ.get("WEATHERAPI_KEY")
    if not api_key:
        error = "Weather API key not set."
    else:
        url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            
            # Format forecast data for template
            forecast_days = data.get("forecast", {}).get("forecastday", [])
            for day in forecast_days:
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                forecast.append({
                    "day_name": date_obj.strftime("%A"),
                    "date": date_obj.strftime("%B %d, %Y"),
                    "temp": int(day["day"]["avgtemp_c"]),
                    "humidity": day["day"]["avghumidity"],
                    "rain": day["day"]["totalprecip_mm"],
                    "description": day["day"]["condition"]["text"]
                })
            
            # Enhanced disease analysis based on weather conditions
            diseases = []
            for i, day in enumerate(forecast_days):
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                conditions = []
                
                temp = day["day"]["avgtemp_c"]
                humidity = day["day"]["avghumidity"]
                rain = day["day"]["totalprecip_mm"]
                min_temp = day["day"]["mintemp_c"]
                max_temp = day["day"]["maxtemp_c"]
                
                # Multiple disease conditions based on different weather patterns
                
                # 1. Fungal Diseases (High humidity conditions)
                if humidity > 80:
                    if 15 <= temp <= 25:
                        conditions.append({
                            "name": "Late Blight (Potato/Tomato)",
                            "risk": "High",
                            "description": f"High humidity ({humidity}%) + cool temps ({temp}°C) favor late blight."
                        })
                    elif 25 <= temp <= 35:
                        conditions.append({
                            "name": "Powdery Mildew",
                            "risk": "High",
                            "description": f"High humidity ({humidity}%) + warm temps ({temp}°C) favor powdery mildew."
                        })
                elif 60 <= humidity <= 80:
                    conditions.append({
                        "name": "Leaf Spot Diseases",
                        "risk": "Medium",
                        "description": f"Moderate humidity ({humidity}%) may cause leaf spots."
                    })
                
                # 2. Bacterial Diseases (Rain + warmth)
                if rain > 2 and temp > 20:
                    conditions.append({
                        "name": "Bacterial Wilt",
                        "risk": "High",
                        "description": f"Rain ({rain}mm) + warm temps ({temp}°C) spread bacterial diseases."
                    })
                elif rain > 0.5:
                    conditions.append({
                        "name": "Bacterial Leaf Spot",
                        "risk": "Medium",
                        "description": f"Light rain ({rain}mm) can cause bacterial infections."
                    })
                
                # 3. Temperature-related issues
                if max_temp > 35:
                    conditions.append({
                        "name": "Heat Stress",
                        "risk": "High",
                        "description": f"High temperature ({max_temp}°C) causes heat stress in crops."
                    })
                elif min_temp < 5:
                    conditions.append({
                        "name": "Frost Damage",
                        "risk": "High",
                        "description": f"Low temperature ({min_temp}°C) risk of frost damage."
                    })
                elif min_temp < 10:
                    conditions.append({
                        "name": "Cold Stress",
                        "risk": "Medium",
                        "description": f"Cool morning temps ({min_temp}°C) may slow growth."
                    })
                
                # 4. Pest-related (based on weather)
                if 20 <= temp <= 30 and humidity < 60 and rain == 0:
                    conditions.append({
                        "name": "Aphid Infestation",
                        "risk": "Medium",
                        "description": f"Dry warm weather ({temp}°C, {humidity}% humidity) favors aphids."
                    })
                
                # 5. Drought stress
                if rain == 0 and humidity < 50:
                    conditions.append({
                        "name": "Drought Stress",
                        "risk": "Medium",
                        "description": f"No rain + low humidity ({humidity}%) causes water stress."
                    })
                
                # If no specific conditions, add a general assessment
                if not conditions:
                    if humidity < 60 and 15 <= temp <= 30 and rain < 1:
                        conditions.append({
                            "name": "Favorable Conditions",
                            "risk": "Low",
                            "description": "Weather conditions are generally favorable for crop growth."
                        })
                
                diseases.append({
                    "day_name": date_obj.strftime("%A"),
                    "date": date_obj.strftime("%B %d, %Y"),
                    "conditions": conditions
                })
            
            # Dynamic precautionary measures based on detected risks
            precautions = []
            
            # Check what diseases were detected to give relevant advice
            all_detected_diseases = []
            for day in diseases:
                for condition in day["conditions"]:
                    all_detected_diseases.append(condition["name"])
            
            # Irrigation advice
            irrigation_tips = ["Water early morning (6-8 AM) to reduce humidity"]
            if "Drought Stress" in all_detected_diseases:
                irrigation_tips.extend([
                    "Increase irrigation frequency during dry periods",
                    "Use mulching to retain soil moisture"
                ])
            if any("Bacterial" in disease for disease in all_detected_diseases):
                irrigation_tips.extend([
                    "Use drip irrigation to minimize leaf wetness",
                    "Avoid overhead sprinklers during rainy periods"
                ])
            precautions.append({"category": "Irrigation", "tips": irrigation_tips})
            
            # Disease management
            disease_tips = ["Monitor plants regularly for early symptoms"]
            if any("Fungal" in disease or "Mildew" in disease or "Blight" in disease for disease in all_detected_diseases):
                disease_tips.extend([
                    "Apply neem oil spray during evening hours",
                    "Use copper-based fungicides for severe infections",
                    "Remove infected plant debris immediately"
                ])
            if any("Bacterial" in disease for disease in all_detected_diseases):
                disease_tips.extend([
                    "Use copper sulfate spray as prevention",
                    "Ensure good air circulation between plants"
                ])
            precautions.append({"category": "Disease Management", "tips": disease_tips})
            
            # Temperature management
            temp_tips = ["Maintain proper plant spacing for air circulation"]
            if "Heat Stress" in all_detected_diseases:
                temp_tips.extend([
                    "Provide shade nets during extreme heat",
                    "Increase watering frequency during hot days"
                ])
            if "Frost Damage" in all_detected_diseases or "Cold Stress" in all_detected_diseases:
                temp_tips.extend([
                    "Cover sensitive plants during cold nights",
                    "Water plants before expected frost"
                ])
            precautions.append({"category": "Temperature Management", "tips": temp_tips})
            
            # General prevention
            precautions.append({
                "category": "General Prevention",
                "tips": [
                    "Use disease-resistant crop varieties",
                    "Practice crop rotation annually",
                    "Maintain field hygiene and sanitation",
                    "Keep farming tools clean and disinfected"
                ]
            })
            
        except Exception as e:
            error = f"Could not fetch weather data: {e}"

    return render_template("weather_templates/results.html",
                          location=location,
                          forecast=forecast,
                          diseases=diseases,
                          precautions=precautions,
                          error=error)

# --- Sustainability (from sustain/app.py & sustain/sustainability.py) ---
# Fertilizers mapping
fertilizers = {
    "urea": {
        "alternative": "🌿 Vermicompost, Panchagavya, Jeevamrutha",
        "benefits": "Improves soil fertility, provides balanced nutrients, enhances microbial activity.",
        "impact": "❌ Urea harms soil long-term. ✅ Organic compost increases soil carbon, reduces cost, and improves resilience.",
        "procedure": """Vermicompost:
1. Prepare shaded pit/container, add waste + dung + worms.
2. Cover, sprinkle water, compost ready in 45–60 days.
Panchagavya:
1. Ferment cow dung, urine, milk, curd, ghee, bananas, jaggery, coconut water.
2. Stir daily for 20 days, dilute before use.
Jeevamrutha:
1. Mix cow dung, urine, jaggery, pulse flour, soil in water.
2. Ferment 5–7 days, apply in irrigation water.""",
        "dosage": "Vermicompost: 2–5 tons/acre; Panchagavya: 3% foliar spray every 15 days; Jeevamrutha: 200 liters/acre every 15 days."
    },
    "dap": {
        "alternative": "🌱 Rock Phosphate + Cow Manure",
        "benefits": "Provides slow-release phosphorus and improves soil structure.",
        "impact": "❌ DAP causes nutrient imbalance. ✅ Rock phosphate enriches soil naturally.",
        "procedure": """Mix rock phosphate powder with cow dung, compost for 30–40 days before application.""",
        "dosage": "Apply 100–150 kg rock phosphate + 1 ton cow manure per acre before sowing."
    },
    "npk": {
        "alternative": "🌿 Green Manure + Farmyard Manure",
        "benefits": "Adds NPK naturally, improves soil structure.",
        "impact": "❌ NPK salts reduce soil microbes. ✅ Green manure supports healthy soil life.",
        "procedure": """Green Manure: Grow sunhemp/dhaincha for 30–40 days, plough in soil.
Farmyard Manure: Collect dung, urine, straw, compost 2–3 months, then apply.""",
        "dosage": "Green manure: 8–10 kg seed/acre; FYM: 5–10 tons/acre before sowing."
    },
    "mop": {
        "alternative": "🌱 Wood Ash, Banana Stem Compost, Seaweed Extract",
        "benefits": "Supplies potassium naturally, improves plant immunity.",
        "impact": "❌ MOP leads to soil salinity. ✅ Wood ash & seaweed are eco-friendly.",
        "procedure": """Wood Ash: Collect and apply near root zone.
Banana Stem Compost: Chop, mix with dung, compost 40 days.
Seaweed Extract: Dilute before spraying.""",
        "dosage": "Wood ash: 100–200 kg/acre; Banana compost: 1–2 tons/acre; Seaweed extract: 50 ml/10 liters water, foliar spray every 20 days."
    },
    "zinc sulphate": {
        "alternative": "🌿 Zinc-rich biofertilizers, Cow Dung, Rock Dust",
        "benefits": "Provides zinc slowly, improves soil microbes.",
        "impact": "❌ Excess ZnSO₄ harms soil. ✅ Natural sources are safer.",
        "procedure": """Apply rock dust or slurry of cow dung with biofertilizers during land prep.""",
        "dosage": "Rock dust: 250–500 kg/acre; Zinc biofertilizer: 1–2 kg/acre mixed with compost."
    }
}

# Pesticides mapping
pesticides = {
    "pesticide": {
        "alternative": "🦗 Neem Oil Spray, Garlic-Chili Extract, Cow Urine Solution",
        "benefits": "Repels harmful insects without killing pollinators.",
        "impact": "❌ Chemical pesticides kill beneficial insects. ✅ Herbal sprays are eco-safe.",
        "procedure": """Neem Oil: Mix neem oil + soap + water, spray evening.
Garlic-Chili Extract: Grind, boil, filter, dilute before spraying.
Cow Urine: Dilute, ferment 3–5 days, spray.""",
        "dosage": "Neem oil: 30 ml/liter water; Garlic-Chili: 100 ml extract/10 liters water; Cow urine: 5 liters urine + 20 liters water per acre spray."
    },
    "insecticide": {
        "alternative": "🐞 Neem Oil, Soap Spray, Intercropping with Marigold",
        "benefits": "Controls pests, supports pollinators, reduces residues.",
        "impact": "❌ Insecticides contaminate food. ✅ Organic methods produce healthier crops.",
        "procedure": """Neem spray & soap spray as repellents; Marigold intercrop to repel pests.""",
        "dosage": "Neem oil: 30 ml/liter water weekly; Soap spray: 20 g/liter water; Marigold: 4000–5000 plants/acre between main crops."
    },
    "carbofuran": {
        "alternative": "🌿 Neem Seed Powder, Trichogramma Bio-control",
        "benefits": "Effective against soil pests safely.",
        "impact": "❌ Highly toxic. ✅ Neem-based products are safe.",
        "procedure": """Neem seeds dried & powdered; sprinkle in soil.
Trichogramma egg cards released in field.""",
        "dosage": "Neem powder: 250 g/10 m² soil; Trichogramma: 10–12 cards/acre every 15 days."
    },
    "monocrotophos": {
        "alternative": "🌱 Herbal Pesticides + Sticky Traps",
        "benefits": "Controls sucking pests safely.",
        "impact": "❌ Deadly. ✅ Herbal solutions protect farmer health.",
        "procedure": """Sticky traps coated with oil/grease; Herbal sprays (neem, garlic).""",
        "dosage": "Sticky traps: 8–10 per acre; Herbal spray: 100 ml decoction/10 liters water every 7–10 days."
    },
    "glyphosate": {
        "alternative": "🌿 Mulching, Hand Weeding, Cow-based Herbicides",
        "benefits": "Controls weeds, improves soil moisture.",
        "impact": "❌ Carcinogenic. ✅ Organic methods save water, enrich soil.",
        "procedure": """Mulch soil with straw/leaves; Hand weed at intervals; Spray fermented cow dung + urine mix.""",
        "dosage": "Mulch: 2–3 tons dry biomass/acre; Hand weeding: every 20–25 days; Cow-based herbicide: 2–3 liters fermented solution in 20 liters water, spray per acre."
    },
    "endosulfan": {
        "alternative": "🐞 Neem Oil, Bacillus thuringiensis (Bt), Bio-control",
        "benefits": "Targets pests safely without harming humans.",
        "impact": "❌ Banned. ✅ Organic methods protect environment & health.",
        "procedure": """Neem spray for sucking pests; Bt spray for caterpillars; Release ladybird beetles.""",
        "dosage": "Neem oil: 30 ml/liter water; Bt powder: 2 g/liter water; Bio-control insects: 2000–3000/acre release."
    },
    "mancozeb": {
        "alternative": "🍄 Neem Decoction, Garlic Extract, Whey Spray",
        "benefits": "Effective against leaf spots naturally.",
        "impact": "❌ Leaves residues. ✅ Herbal sprays are safe.",
        "procedure": """Boil neem leaves; make garlic paste decoction; dilute whey for spraying.""",
        "dosage": "Neem decoction: 500 ml/10 liters water; Garlic extract: 50 ml/10 liters water; Whey: 1 liter whey in 9 liters water, foliar spray every 10 days."
    },
    "captan": {
        "alternative": "🌿 Cow Urine + Asafoetida Mixture",
        "benefits": "Prevents seedling rot naturally.",
        "impact": "❌ Contaminates soil. ✅ Cow-based solutions promote soil life.",
        "procedure": """Mix cow urine + asafoetida in water, apply to seedlings.""",
        "dosage": "Cow urine mix: 1 liter urine + 10 g asafoetida + 10 liters water, applied at seedling stage."
    }
}

def suggest_fertilizer(input_text):
    input_text = input_text.lower().strip()
    if input_text in fertilizers:
        return fertilizers[input_text]
    return {
        "alternative": "✅ Use compost, green manure & biofertilizers.",
        "benefits": "Supports soil fertility and sustainable farming.",
        "impact": "Healthy soil, better yields, safe food.",
        "procedure": "General composting/vermicompost methods can be used.",
        "dosage": "Compost: 2–5 tons/acre applied before sowing."
    }

def suggest_pesticide(input_text):
    input_text = input_text.lower().strip()
    if input_text in pesticides:
        return pesticides[input_text]
    return {
        "alternative": "✅ Use Neem, Garlic-Chili sprays, or bio-control methods.",
        "benefits": "Safe, eco-friendly, and cost-effective.",
        "impact": "Protects crops, soil, pollinators, and your health.",
        "procedure": "Neem spray or garlic extract applied weekly in evening.",
        "dosage": "Neem oil: 30 ml/liter water; Garlic extract: 100 ml/10 liters water."
    }

@app.route("/sustainability", methods=["GET", "POST"])
def sustainability():
    fert_suggestion = None
    pest_suggestion = None
    selected_fertilizer = ""
    selected_pesticide = ""

    if request.method == "POST":
        selected_fertilizer = request.form.get("fertilizer", "").strip()
        selected_pesticide = request.form.get("pesticide", "").strip()

        # Fertilizer suggestion
        if selected_fertilizer:
            fert_suggestion = suggest_fertilizer(selected_fertilizer)

            # Ensure all keys exist to avoid Jinja errors
            fert_suggestion.setdefault("procedure", "ℹ️ Procedure details not available.")
            fert_suggestion.setdefault("dosage", "ℹ️ Dosage information not available.")

        # Pesticide suggestion
        if selected_pesticide:
            pest_suggestion = suggest_pesticide(selected_pesticide)

            # Ensure all keys exist to avoid Jinja errors
            pest_suggestion.setdefault("procedure", "ℹ️ Procedure details not available.")
            pest_suggestion.setdefault("dosage", "ℹ️ Dosage information not available.")

    return render_template(
        "sustain_index.html",
        fertilizers=list(fertilizers.keys()),
        pesticides=list(pesticides.keys()),
        fert_suggestion=fert_suggestion,
        pest_suggestion=pest_suggestion,
        selected_fertilizer=selected_fertilizer,
        selected_pesticide=selected_pesticide
    )


# --- Market Price Integration (from price/app.py) ---
def fetch_market_prices(crop_name):
    # Map crop names to Agmarknet commodity names
    commodity_map = {
        'Tomato': 'Tomato',
        'Potato': 'Potato',
        'Corn': 'Maize',
    }
    commodity = commodity_map.get(crop_name, crop_name)
    api_key = os.environ.get('AGMARKNET_API_KEY')
    endpoint = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'
    today = datetime.today()
    last_7_days = [(today - timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
    params = {
        'api-key': api_key or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
        'format': 'json',
        'limit': 100,
        'filters[commodity]': crop_name
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()
        records = result.get('records', [])
        filtered = [r for r in records if r.get('arrival_date') in last_7_days]
        filtered.sort(key=lambda x: datetime.strptime(x.get('arrival_date'), '%d/%m/%Y'), reverse=True)
        data = []
        for r in filtered:
            try:
                price = int(float(r.get('modal_price')))
            except:
                continue
            data.append({
                'date': r.get('arrival_date'),
                'price': price,
                'market': r.get('market'),
                'state': r.get('state'),
            })
        return data
    except Exception as e:
        print('API error:', e)
        return []

@app.route('/market', methods=['GET', 'POST'])
def market():
    if request.method == 'POST':
        crop_name = request.form.get('crop') or (request.json and request.json.get('crop'))
        data = fetch_market_prices(crop_name)
        return jsonify(data)
    return render_template('price_templates/market.html')

@app.route("/animal-husbandry")
def animal_husbandry():
    return render_template("animal_index.html")

@app.route("/animal_husbandary_pages/dairy.html")
def dairy_farming():
    return render_template("animal_husbandary_pages/dairy.html")

@app.route("/animal_husbandary_pages/poultry.html")
def poultry_farming():
    return render_template("animal_husbandary_pages/poultry.html")

@app.route("/animal_husbandary_pages/pisciculture.html")
def pisciculture():
    return render_template("animal_husbandary_pages/pisciculture.html")

@app.route("/animal_husbandary_pages/apiculture.html")
def apiculture():
    return render_template("animal_husbandary_pages/apiculture.html")

@app.route("/animal_husbandary_pages/sericulture.html")
def sericulture():
    return render_template("animal_husbandary_pages/sericulture.html")

@app.route("/animal_husbandary_pages/breed.html")
def breed_detail():
    return render_template("animal_husbandary_pages/breed.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/index")
def index():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
