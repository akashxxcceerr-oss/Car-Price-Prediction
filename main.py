from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Model trained in Untitled (1).ipynb (Current Year = 2020, raw Kms_Driven)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

CURRENT_YEAR = 2026  # must match 'Current Year' used in the training notebook


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    try:
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
    except (KeyError, ValueError):
        return render_template('index.html', pred="Please enter valid numbers in all fields")

    no_year = CURRENT_YEAR - Year

    # Fuel: CNG is the baseline dropped by get_dummies(drop_first=True) -> both 0
    fuel = request.form['Fuel_Type_Petrol']
    Fuel_Type_Petrol = 1 if fuel == 'Petrol' else 0
    Fuel_Type_Diesel = 1 if fuel == 'Diesel' else 0

    # Seller: Dealer is the baseline
    Seller_Type_Individual = 1 if request.form['Seller_Type_Individual'] == 'Individual' else 0

    # Transmission: Automatic is the baseline
    Transmission_Manual = 1 if request.form['Transmission_Manual'] == 'Manual' else 0

    # Same column order as X in the notebook:
    # Present_Price, Kms_Driven, Owner, no_year, Fuel_Type_Diesel,
    # Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual
    features = [[Present_Price, Kms_Driven, Owner, no_year,
                 Fuel_Type_Diesel, Fuel_Type_Petrol,
                 Seller_Type_Individual, Transmission_Manual]]

    prediction = model.predict(features)
    output = round(prediction[0], 2)

    if output < 0:
        return render_template('index.html', pred="Sorry you cannot sell this car")
    return render_template('index.html', pred="You Can Sell The Car at {} lakhs".format(output))


if __name__ == "__main__":
    app.run(debug=True)
