from flask import Flask, render_template, request, abort

app = Flask(__name__)

# In-memory storage for upload submissions
submissions = []

# Real NGO data with official donation links
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
}

# Sample Markets data
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
]

@app.route("/")
def home():
    return render_template("index.html")

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

    return render_template("upload.html", success_message=success_message, submissions=submissions)

@app.route("/markets")
def markets():
    return render_template("markets.html", markets=MARKETS_DATA)

@app.route("/ngos")
def ngos():
    ngos_list = list(NGO_DATA.values())
    return render_template("ngos.html", ngos=ngos_list)

@app.route("/ngos/<slug>")
def ngo_detail(slug: str):
    ngo = NGO_DATA.get(slug)
    if not ngo:
        abort(404)
    return render_template("ngo_detail.html", ngo=ngo)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
