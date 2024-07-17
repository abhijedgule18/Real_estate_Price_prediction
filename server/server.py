from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        response = jsonify({
            'locations': util.get_location_names()
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            return jsonify(
                {'error': 'POST request required for prediction'}), 400  # Bad request for GET on prediction route

        # Process form data for POST request
        total_sqft = float(request.form.get('total_sqft'))
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bath'))

        response = jsonify({
            'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except (ValueError, KeyError) as e:
        print(f"Error processing form data: {e}")
        return jsonify({'error': 'Invalid input data'}), 400  # Bad request


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)  # Enable debug mode for easier error identification
