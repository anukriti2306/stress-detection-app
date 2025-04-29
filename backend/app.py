import pickle
from flask import Flask, request, jsonify

# Load the trained model and vectorizer
model_file = 'model/final_model_v2.bin'  # Matches updated model filename

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Expected features (must match training script)
features = ['humidity', 'temperature', 'step_count']

# Initialize Flask app
app = Flask('stress_level_api')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validate and extract input features
    try:
        input_data = {key: data[key] for key in features}
    except KeyError as e:
        return jsonify({'error': f'Missing feature: {e}'}), 400

    # Transform and predict
    X = dv.transform([input_data])
    y_pred = model.predict(X)

    # Optionally map numeric prediction to label
    label_map = {0: 'Low', 1: 'Normal', 2: 'High'}
    prediction_label = label_map.get(int(y_pred[0]), 'Unknown')

    # Return result
    return jsonify({
        'stress_level_code': int(y_pred[0]),
        'stress_level_label': prediction_label
    })

# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)  # Changed port to 5050
