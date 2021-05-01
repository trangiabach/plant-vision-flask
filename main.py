import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
import pymysql
pymysql.install_as_MySQLdb()
from flask import jsonify
from tensorflow.keras.preprocessing import image
from flask_cors import CORS
from models import db
from models.Models import Disease

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__, static_folder='../client/dist/',    static_url_path='/')

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://sql6409422:YQYYXyF9sw@sql6.freemysqlhosting.net/sql6409422"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'

model =tf.keras.models.load_model('detect.h5',compile=False)


def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(f.filename))
        f.save(file_path)
        print(basepath)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        disease_class = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        a = preds[0]
        ind=np.argmax(a)
        print('Prediction:', disease_class[ind])
        result=disease_class[ind]
        query = Disease.query.filter_by(name=result).first()
        return jsonify({
            "result": result,
            "image": query.url,
            "symptoms": query.symptoms,
            "causes": query.causes,
            "solutions": query.solutions,
        })
    if request.method == "GET":
        disease_class = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        return jsonify({
            "diseases": ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        })
    return None

@app.route('/disease', methods=['POST'])
def get_disease():
    req = request.get_json()
    result = req["name"]
    query = Disease.query.filter_by(name=result).first()
    return jsonify({
        "result": result,
        "image": query.url,
        "symptoms": query.symptoms,
        "causes": query.causes,
        "solutions": query.solutions
    })




if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    app.run()
