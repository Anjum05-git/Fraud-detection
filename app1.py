from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load the model
model = joblib.load("model.pkl")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple login validation (use a database in real apps)
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials try again")
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")
@app.route("/detect", methods=["GET", "POST"])
def detect():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)
            preds = model.predict(df)
            if len(preds) == 1:
                result = "It is a Fraud " if preds[0] == 1 else "It is  Not Fraud"
            else:
                result = f"Out of {len(preds)} records, {sum(preds)} predicted as fraud."
            # Pass image filename to template
            return render_template("detect.html", result=result, image_file="roc_result.png")
    return render_template("detect.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
