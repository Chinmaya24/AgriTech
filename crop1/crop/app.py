from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import sqlite3
from flask import g

app = Flask(__name__)
DATABASE = 'community.db'

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
model = load_model("model/plant_disease_model.h5", compile=False)

# Class names
class_names = ['Tomato-Bacterial_spot', 'Potato-Barly blight', 'Corn-Common_rust']

# Remedies with detailed guidance
remedies = {
    'Tomato-Bacterial_spot': {
        "Treatment": [
            "Remove infected leaves.",
            "Spray copper-based fungicide every 7-10 days.",
            "Neem oil can be used as an organic alternative."
        ],
        "Prevention": [
            "Use disease-free seeds.",
            "Maintain proper spacing between plants.",
            "Rotate crops yearly."
        ],
        "Fertilizer Advice": [
            "Apply Nitrogen 20kg/acre + Potassium 10kg/acre.",
            "Neem-based organic fertilizer optional."
        ],
        "Watering Tips": [
            "Avoid overhead irrigation.",
            "Water early morning."
        ],
        "Harvest Advice": [
            "Harvest promptly to avoid contact with infected foliage.",
            "Discard severely infected fruits."
        ],
        "Extra Tips": [
            "Monitor plants regularly.",
            "Maintain good ventilation in greenhouses."
        ]
    },
    'Potato-Barly blight': {
        "Treatment": [
            "Apply fungicides like mancozeb or chlorothalonil.",
            "Remove severely affected plants."
        ],
        "Prevention": [
            "Plant resistant varieties.",
            "Practice crop rotation.",
            "Space plants adequately."
        ],
        "Fertilizer Advice": [
            "Use balanced NPK fertilizer: N15:P15:K15.",
            "Compost can improve soil health."
        ],
        "Watering Tips": [
            "Irrigate in the morning.",
            "Avoid waterlogging."
        ],
        "Harvest Advice": [
            "Harvest when foliage is dry.",
            "Store in cool, dry conditions."
        ],
        "Extra Tips": [
            "Destroy volunteer plants.",
            "Monitor brown lesions on leaves."
        ]
    },
    'Corn-Common_rust': {
        "Treatment": [
            "Remove heavily infected plants.",
            "Apply azoxystrobin fungicide.",
            "Sulfur sprays for organic control."
        ],
        "Prevention": [
            "Plant resistant hybrids.",
            "Rotate crops.",
            "Maintain field sanitation."
        ],
        "Fertilizer Advice": [
            "Apply NPK 16:16:16 as basal dose.",
            "Top-dress with Nitrogen mid-growth."
        ],
        "Watering Tips": [
            "Avoid late evening irrigation.",
            "Reduce leaf wetness."
        ],
        "Harvest Advice": [
            "Harvest when kernels are fully mature.",
            "Remove debris post-harvest."
        ],
        "Extra Tips": [
            "Inspect lower leaves regularly.",
            "Improve airflow between plants.",
            "Avoid overcrowding."
        ]
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

# Call this once to initialize the database
init_db()

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    disease = None
    remedy_info = None
    filename = None

    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename != "":
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Preprocess image
            img = Image.open(filepath).convert('RGB').resize((256, 256))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
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

    return render_template(
        "index.html",
        disease=disease,
        remedy=remedy_info,
        result=bool(disease),
        filename=filename
    )

# In-memory storage for posts
posts = [
    {
        "id": 1,
        "disease": "Tomato Blight",
        "title": "Leaves turning yellow",
        "content": "What should I do?",
        "comments": ["Try copper spray", "Rotate crops"]
    }
]

@app.route('/community')
def community():
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    return render_template('community.html', posts=posts)

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

if __name__ == "__main__":
    app.run(debug=True)
