# 🌱 Krushi Snehii - AI-Powered Agriculture Platform

Krushi Snehii is a comprehensive AI-powered agriculture platform that helps farmers with early crop disease detection, community networking, market access, weather forecasting, sustainability advice, and animal husbandry guidance. It integrates machine learning, community engagement, and marketplace tools into one ecosystem for sustainable farming.

## 🚀 Features

- 🌾 **AI Crop Disease Detection** - Upload crop leaf images for AI-powered disease prediction and treatment suggestions
- 👨‍👩‍👧‍👦 **FarmConnect** - Community platform for farmers to connect, share posts, and join NGOs
- 💬 **Farmer Community** - Discussion forum for farmers to interact and share experiences
- 🛒 **Market Access** - Connect with local markets and NGOs for support and selling
- 🌤️ **Weather Forecasting** - Get local weather updates and disease risk analysis
- 🌿 **Sustainability Advisor** - Find organic alternatives for fertilizers and pesticides
- 🐄 **Animal Husbandry Guide** - Comprehensive guide for dairy, poultry, fish farming, and more
- 💧 **Hydroponics Advisor** - Learn and build hydroponic farming systems
- 🔥 **Gobar Gas Calculator** - Biogas education and community marketplace
- 📈 **Market Price Tracker** - Real-time crop price monitoring

## 📂 Project Structure

```
AgriTech/
│
├── app.py                              # Main Flask application
├── LICENSE
├── README.md
├── .env                               # Environment variables (API keys)
├── requirements.txt
│
├── crop1/                             # AI Crop Disease Module
│   └── crop/
│       ├── app.py
│       ├── community.db               # SQLite database for community
│       ├── requirements.txt
│       ├── model/
│       │   └── plant_disease_model.h5 # Trained ML model
│       ├── templates/
│       │   ├── community.html
│       │   ├── index.html
│       │   ├── new_post.html
│       │   └── post_detail.html
│       └── uploads/                   # User uploaded images
│           ├── cknpic.jpg
│           ├── corn.jpeg
│           ├── potato.jpeg
│           └── tomato.jpeg
│
├── FarmConnect/                       # Farmer Community Module
│   ├── app.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── markets.html
│       ├── ngo_detail.html
│       ├── ngos.html
│       └── upload.html
│
├── gobar-gas-app/                     # Biogas Calculator Module
│   ├── app.js
│   ├── index.html
│   ├── manifest.json
│   ├── styles.css
│   ├── sw.js
│   ├── assets/
│   └── translations/
│       └── en.json
│
├── hydro/                             # Hydroponics Module
│   ├── app.py
│   ├── hydro_utils.py
│   ├── __pycache__/
│   │   └── hydro_utils.cpython-310.pyc
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       ├── base.html
│       ├── hydro_info.html
│       ├── hydro_nutrients.html
│       ├── hydro_recommend.html
│       └── hydro_setup.html
│
├── price/                             # Market Price Module
│   └── app.py
│
├── sustain/                           # Sustainability Module
│   ├── app.py
│   └── sustainability.py
│
├── weather/                           # Weather Forecasting Module
│   ├── app.py
│   ├── README.md
│   ├── requirements.txt
│   ├── setup.py
│   ├── __pycache__/
│   │   └── app.cpython-313.pyc
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── results.html
│
├── static/                            # Static Assets
│   ├── gobar_app.js
│   ├── gobar_styles.css
│   ├── main-home.css
│   ├── main-home.js
│   │
│   ├── assets/                        # Images and Media
│   │   ├── co2.jpg
│   │   ├── cropdes.jpg
│   │   ├── croptest.jpg
│   │   ├── f2f.jpg
│   │   ├── facebook.jpg
│   │   ├── Farmer.jpg
│   │   ├── Foodsafety.jpg
│   │   ├── gettyimages-1340420992-640_adpp.mp4
│   │   ├── gobar.jpg
│   │   ├── hydrophonics.jpg
│   │   ├── instagram.jpg
│   │   ├── logo.jpg
│   │   ├── marketpriselogo.png
│   │   ├── sustainability.png
│   │   ├── weather.jpg
│   │   ├── X.jpg
│   │   ├── Youtube.jpg
│   │   └── animal_husbandary/
│   │       ├── aseel_chicken.png
│   │       ├── catla_fish.png
│   │       ├── gir_cow.png
│   │       ├── holstein_friesian.png
│   │       ├── indian_hive_bee.png
│   │       ├── jersey_cow.png
│   │       ├── kadaknath.png
│   │       ├── mulberry_silkworm.png
│   │       ├── murrah_buffalo.png
│   │       ├── rock_bee.png
│   │       ├── rohu_fish.png
│   │       ├── tasar_silkworm.png
│   │       ├── tilapia.png
│   │       └── white_leghorn.png
│   │
│   ├── animal_husbandary_static/      # Animal Husbandry Styles
│   │   ├── script.js
│   │   └── style.css
│   │
│   ├── farmconnect_static/            # FarmConnect Styles
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   │
│   ├── hydro_static/                  # Hydroponics Styles
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   │
│   └── sustain_static/                # Sustainability Styles
│       └── style.css
│
└── templates/                         # HTML Templates
    ├── animal_index.html              # Animal Husbandry Home
    ├── gobar_index.html               # Biogas Calculator
    ├── main-home.html                 # Main Dashboard
    ├── sustain_index.html             # Sustainability Advisor
    │
    ├── animal_husbandary_pages/       # Animal Farming Pages
    │   ├── apiculture.html            # Beekeeping Guide
    │   ├── breed.html                 # Breed Details
    │   ├── dairy.html                 # Dairy Farming
    │   ├── pisciculture.html          # Fish Farming
    │   ├── poultry.html               # Poultry Farming
    │   └── sericulture.html           # Silk Farming
    │
    ├── crop_templates/                # Crop Disease Templates
    │   ├── community.html
    │   ├── index.html
    │   ├── new_post.html
    │   └── post_detail.html
    │
    ├── farmconnect_templates/         # FarmConnect Templates
    │   ├── base.html
    │   ├── index.html
    │   ├── markets.html
    │   ├── ngo_detail.html
    │   ├── ngos.html
    │   └── upload.html
    │
    ├── hydro_templates/               # Hydroponics Templates
    │   ├── base.html
    │   ├── hydro_info.html
    │   ├── hydro_nutrients.html
    │   ├── hydro_recommend.html
    │   └── hydro_setup.html
    │
    ├── price_templates/               # Market Price Templates
    │   ├── base.html
    │   └── market.html
    │
    └── weather_templates/             # Weather Forecast Templates
        ├── base.html
        ├── index.html
        └── results.html
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **AI/ML**: TensorFlow, Keras
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: WeatherAPI, Government Data APIs
- **Styling**: Bootstrap, Custom CSS

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AgriTech.git
   cd AgriTech
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key_here
   WEATHERAPI_KEY=your_weather_api_key
   AGMARKNET_API_KEY=your_market_api_key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📱 Features Overview

### 🌾 AI Crop Disease Detection
- Upload crop leaf images
- AI-powered disease identification
- Treatment recommendations
- Supports Tomato, Potato, and Corn crops

### 🌤️ Weather & Disease Risk Analysis
- 3-day weather forecasting
- Disease risk assessment based on weather conditions
- Farmer-specific recommendations
- Location-based predictions

### 🌿 Sustainability Advisor
- Organic alternatives to chemical fertilizers
- Eco-friendly pesticide substitutes
- Detailed application procedures
- Environmental impact analysis

### 🐄 Animal Husbandry Guide
- **Dairy Farming**: Cow breeds, milking, feeding
- **Poultry Farming**: Chicken breeds, housing, biosecurity
- **Pisciculture**: Fish farming, pond management
- **Apiculture**: Beekeeping, honey production
- **Sericulture**: Silkworm rearing, cocoon production

### 💧 Hydroponics System
- Nutrient solution calculator
- System setup guidance
- Plant recommendations
- Resource optimization

### 📈 Market Integration
- Real-time crop prices
- Market trend analysis
- NGO and buyer connections
- Selling opportunities

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Project Lead**: [Your Name]
- **AI/ML Developer**: [Team Member]
- **Backend Developer**: [Team Member]
- **Frontend Developer**: [Team Member]

## 📞 Contact

- **Email**: info@krushisnehii.com
- **Phone**: +91-12345-67890
- **Website**: [www.krushisnehii.com](http://www.krushisnehii.com)

## 🙏 Acknowledgments

- Thanks to the farming community for their valuable feedback
- Weather data provided by WeatherAPI
- Market data from Government of India APIs
- Plant disease dataset contributors

---

**Made with ❤️ for farmers by the Krushi Snehii team**