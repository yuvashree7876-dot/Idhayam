from flask import Flask, render_template, request
import sqlite3
import pickle

app = Flask(__name__)

# Load Machine Learning Model
model = pickle.load(open("heart_model.pkl", "rb"))


# Create Database
def create_database():

    conn = sqlite3.connect("heart_disease.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            sex INTEGER,
            cp INTEGER,
            trestbps INTEGER,
            chol INTEGER,
            fbs INTEGER,
            restecg INTEGER,
            thalach INTEGER,
            exang INTEGER,
            oldpeak REAL,
            slope INTEGER,
            ca INTEGER,
            prediction TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["age"])
    sex = int(request.form["sex"])
    cp = int(request.form["cp"])
    trestbps = int(request.form["trestbps"])
    chol = int(request.form["chol"])
    fbs = int(request.form["fbs"])
    restecg = int(request.form["restecg"])
    thalach = int(request.form["thalach"])
    exang = int(request.form["exang"])
    oldpeak = float(request.form["oldpeak"])
    slope = int(request.form["slope"])
    ca = int(request.form["ca"])

    data = [[
        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca
    ]]

    prediction = model.predict(data)[0]

    if prediction == 1:
        result = "Higher Risk of Heart Disease"
    else:
        result = "Lower Risk of Heart Disease"

    # Store data in database
    conn = sqlite3.connect("heart_disease.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients
        (age, sex, cp, trestbps, chol, fbs,
         restecg, thalach, exang, oldpeak,
         slope, ca, prediction)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        age, sex, cp, trestbps, chol, fbs,
        restecg, thalach, exang, oldpeak,
        slope, ca, result
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
