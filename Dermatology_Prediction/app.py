from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load('dermatology_model.pkl')


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin123':
        return render_template('predict.html')

    return "Invalid Username or Password"


@app.route('/predict', methods=['POST'])
def predict():

    values = []

    for i in range(1, 35):
        value = float(request.form[f'feature{i}'])
        values.append(value)

    data = np.array([values])

    prediction = model.predict(data)[0]

    disease_map = {
        1: "Psoriasis",
        2: "Seboreic Dermatitis",
        3: "Lichen Planus",
        4: "Pityriasis Rosea",
        5: "Chronic Dermatitis",
        6: "Pityriasis Rubra Pilaris"
    }

    result = disease_map.get(
        prediction,
        "Unknown Disease"
    )

    return render_template(
        'result.html',
        prediction_text=result
    )


if __name__ == '__main__':
    app.run(debug=True)