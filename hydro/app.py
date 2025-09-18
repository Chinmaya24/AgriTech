from flask import Flask, render_template, request
from hydro_utils import recommend_system, nutrient_recipe


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("hydro_info.html", title="Hydroponics Info")

    @app.route("/recommend", methods=["GET", "POST"])
    def recommend():
        result = None
        if request.method == "POST":
            crop = request.form.get("crop", "").strip()
            space = request.form.get("space", "").strip()
            budget = request.form.get("budget", "").strip()
            lighting = request.form.get("lighting", "").strip()
            result = recommend_system(crop, space, budget, lighting)
        return render_template("hydro_recommend.html", title="Recommendation Tool", result=result)

    @app.route("/nutrients", methods=["GET", "POST"])
    def nutrients():
        mix = None
        if request.method == "POST":
            crop = request.form.get("crop", "").strip()
            mix = nutrient_recipe(crop)
        return render_template("hydro_nutrients.html", title="Nutrient Mix", mix=mix)

    @app.route("/setup")
    def setup_page():
        return render_template("hydro_setup.html", title="Hydroponics Setup & Materials")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


