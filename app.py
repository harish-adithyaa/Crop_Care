from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = load_model('/Users/loghit73/Downloads/Crop-Care-master/crop_care.h5')

# List of classes for the model
classes = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/try')
def display():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            img_array = prepare_image(file_path)
            prediction = model.predict(img_array)
            os.remove(file_path)
            class_result = np.argmax(prediction, axis=1)
            disease = classes[class_result[0]]
            return jsonify({'disease': disease})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
