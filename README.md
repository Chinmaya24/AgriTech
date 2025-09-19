🌱 Krushi Snehii

Krushi Snehii is an AI-powered agriculture platform that helps farmers with early crop disease detection, community networking, and market access.
It integrates machine learning, community engagement, and marketplace tools into one ecosystem for sustainable farming.

🚀 Features

🌾 Crop Disease Detection
Upload crop leaf images → AI model predicts disease and suggests remedies.
(Supports Tomato, Potato, Corn using Plant Diseases (3 Types)
).

👨‍👩‍👧‍👦 FarmConnect
Farmers can connect, share posts, join NGOs, and explore market opportunities.

💬 Farmer Community
Discussion forum where farmers facing similar issues can interact and share experiences.

🛒 Market Access
Farmers can connect with local markets and NGOs for support and selling.

📂 Project Structure

AgriTech/
│
├── app.py
├── LICENSE
├── README.md
│
├── crop1/
│   └── crop/
│       ├── app.py
│       ├── community.db
│       ├── requirements.txt
│       ├── model/
│       │   └── plant_disease_model.h5
│       ├── templates/
│       │   ├── community.html
│       │   ├── index.html
│       │   ├── new_post.html
│       │   └── post_detail.html
│       └── uploads/
│           ├── Bharatiya Antariksh Hackathon 2025 Idea Submission PPT[1].pptx
│           ├── cknpic.jpg
│           ├── corn.jpeg
│           ├── crn.jpg
│           ├── PLACEMENT POSTER.png
│           ├── potato.jpeg
│           ├── pto.jpg
│           ├── tmt.jpg
│           ├── toamto1.jpeg
│           ├── tomato.jpeg
│
├── FarmConnect/
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
├── gobar-gas-app/
│   ├── app.js
│   ├── index.html
│   ├── manifest.json
│   ├── styles.css
│   ├── sw.js
│   ├── assets/
│   └── translations/
│       └── en.json
│
├── hydro/
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
├── static/
│   ├── gobar_app.js
│   ├── gobar_styles.css
│   ├── main-home.css
│   ├── main-home.js
│   ├── assets/
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
│   │   ├── weather.jpg
│   │   ├── X.jpg
│   │   ├── Youtube.jpg
│   ├── farmconnect_static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── hydro_static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── templates/
│   ├── gobar_index.html
│   ├── main-home.html
│   ├── crop_templates/
│   │   ├── community.html
│   │   ├── index.html
│   │   ├── new_post.html
│   │   └── post_detail.html
│   ├── farmconnect_templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── markets.html
│   │   ├── ngo_detail.html
│   │   ├── ngos.html
│   │   └── upload.html
│   ├── hydro_templates/
│   │   ├── base.html
│   │   ├── hydro_info.html
│   │   ├── hydro_nutrients.html
│   │   ├── hydro_recommend.html
│   │   └── hydro_setup.html
│   └── weather_templates/
│       ├── base.html
│       ├── index.html
│       └── results.html
│
└── weather/
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── __pycache__/
    │   └── app.cpython-313.pyc
    └── templates/
        ├── base.html
        ├── index.html
        └── results.html

🛠️ Installation & Setup
1. Clone the Repository
git clone https://github.com/your-username/Krushi_Snehii.git
cd Krushi_Snehii-main

2. Install Dependencies
pip install -r crop1/crop/requirements.txt

3. Run the Applications

Main App

python app.py


FarmConnect (Community & Market)

cd FarmConnect
python app.py


Crop Disease Detection

cd crop1/crop
python app.py

📊 Dataset

We use the Plant Diseases (3 Types)
 dataset, which contains labeled images of:

🌽 Corn (Healthy / Diseased)

🥔 Potato (Healthy / Diseased)

🍅 Tomato (Healthy / Diseased)

Download via kagglehub:

import kagglehub

# Download latest version
path = kagglehub.dataset_download("kashyapankush/plant-diseases-3-types")
print("Path to dataset files:", path)

🧠 Model Training (Optional)

To retrain the model:

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

data_dir = path  # from kagglehub
img_size = (128, 128)
batch_size = 32

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Example model
model = tf.keras.applications.MobileNetV2(input_shape=(128,128,3), weights=None, classes=6)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train_data, validation_data=val_data, epochs=10)

# Save model
model.save("plant_disease_model.h5")


Place the trained model inside:

crop1/crop/model/plant_disease_model.h5

📸 Screenshots

Disease detection upload page

Farmer community forum

Market & NGO connect

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

📜 License

This project is licensed under the MIT License
.
