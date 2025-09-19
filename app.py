from flask import Flask, render_template, request, send_from_directory, redirect, url_for, abort, g
import os
import sqlite3
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from dotenv import load_dotenv

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
    return render_template('new_post.html')

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
    city = None
    error = None
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            import requests
            import os
            api_key = os.environ.get("WEATHERAPI_KEY")
            if not api_key:
                error = "Weather API key not set."
            else:
                url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                    weather_data = resp.json()
                except Exception as e:
                    error = f"Could not fetch weather: {e}"
    return render_template("weather_templates/index.html", city=city, error=error, weather=weather_data)

@app.route("/results", methods=["POST"])
def weather_results():
    location = request.form["location"]
    forecast = []
    diseases = []
    precautions = []
    error = None

    # Fetch weather data from WeatherAPI
    import requests, os
    api_key = os.environ.get("WEATHERAPI_KEY")
    if not api_key:
        error = "Weather API key not set."
    else:
        url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            # Example: extract 3-day forecast
            forecast = data.get("forecast", {}).get("forecastday", [])
            # TODO: Add your disease risk analysis logic here
            # diseases = ...
            # precautions = ...
        except Exception as e:
            error = f"Could not fetch weather: {e}"

    return render_template("weather_templates/results.html",
                          location=location,
                          forecast=forecast,
                          diseases=diseases,
                          precautions=precautions,
                          error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
