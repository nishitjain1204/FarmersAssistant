from flask import Flask , jsonify,request,Markup
import json
from flask_restx import Resource, Api
from newsscrapper import scraper
from werkzeug.utils import secure_filename
from disease_predictions import predict_image
from utils.disease import disease_dic
import os
import pickle
import requests
import numpy as np

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = '86d30f802c60961313cc1f87ece01ae8'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    print(x)
    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None




def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)

@api.route('/news')
class news(Resource):
    def get(self):
        return jsonify(scraper())

@api.route('/')
class home(Resource):
    def get(self):
        return {'hello':'world'}

@api.route('/disease-predict')
class diseasePredict(Resource):
    def get(self):
        # print(weather_fetch('Kalyan'))
        return {'method':request.method}
    def post(self):
            # check if the post request has the file part
            if 'file' not in request.files:
                return {'error':'No file part'}
            file = request.files['file']
            if file.filename == '':
                return {'error':'no file selected'}
            if file and allowed_file(file.filename):
                print(file)
                filename = secure_filename(file.filename)
                img = file.read()
                prediction = predict_image(img)
                with open('disease_dic.json') as json_file:
                    data = json.load(json_file)
                # print(data)
                
            
                    #"Crop</b>:([a-zA-Z\ ]*)<br/>Disease:([a-zA-Z\ ]*)[<br]*"gm
                # prediction = disease_dic[prediction].strip().split('<br/>')
                return {'prediction':data[prediction]}

@api.route('/crop-predict')

class cropPredict(Resource):
    def post(self):
        datas = json.loads(request.data)
        print(datas)
        N = int(datas['nitrogen'])
        P = int(datas['phosphorous'])
        K = int(datas['pottasium'])
        ph = float(datas['ph'])
        rainfall = float(datas['rainfall'])
        city = str(datas['city'])

        # state = request.form.get("stt")
        

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            return {'prediction':final_prediction}
        else:
            return {'error':'weather_error'}


                

        
        

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)