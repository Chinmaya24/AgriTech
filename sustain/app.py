from flask import Flask, render_template, request
from sustainability import suggest_fertilizer, suggest_pesticide, fertilizers, pesticides

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    fert_suggestion = None
    pest_suggestion = None
    selected_fertilizer = ""
    selected_pesticide = ""

    if request.method == "POST":
        selected_fertilizer = request.form.get("fertilizer")
        selected_pesticide = request.form.get("pesticide")

        if selected_fertilizer:
            fert_suggestion = suggest_fertilizer(selected_fertilizer)
        if selected_pesticide:
            pest_suggestion = suggest_pesticide(selected_pesticide)

    return render_template("index.html",
                           fertilizers=list(fertilizers.keys()),
                           pesticides=list(pesticides.keys()),
                           fert_suggestion=fert_suggestion,
                           pest_suggestion=pest_suggestion,
                           selected_fertilizer=selected_fertilizer,
                           selected_pesticide=selected_pesticide)

if __name__ == "__main__":
    app.run(debug=True)
