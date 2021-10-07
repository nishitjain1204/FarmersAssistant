from flask import Flask , jsonify,request,Markup
import json
from flask_restx import Resource, Api
from newsscrapper import scraper
from werkzeug.utils import secure_filename
from disease_predictions import predict_image
from utils.disease import disease_dic
from utils.fertilizer import fertilizer_dic
import os
import pickle
import requests
import numpy as np
import pandas as pd

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

def image_download(url):
    img_data = requests.get(url).content
    print(type(img_data))
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    file = open('image_name.jpg','rb')
    return file.read()
    

    # with open('image_name.jpg', 'wb') as handler:
    #     handler.write(img_data)


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
            print(request.get_data())
            # if 'imageUrl' in request.data:
            #     data = json.loads(request.data)
            #     print(data)
            #     img = data['imageUrl']
            if 'file' not in request.files:
                data = json.loads(request.data)
                print(data)
                if 'imageUrl' in data:
                    img = data['imageUrl']
                    img = image_download(img)
                    print('Via android',type(img))
                    prediction = predict_image(img)
                    with open('disease_dic.json') as json_file:
                        data = json.load(json_file)
            
                    print(data[prediction])      
                    return data[prediction]
                    # return {'prediction':data[prediction]}
                else:
                    return {'error':'No file part'}
            else:
                file = request.files['file']
                if file.filename == '':
                    return {'error':'no file selected'}
                if file and allowed_file(file.filename):
                    print(file)
                    filename = secure_filename(file.filename)
                    img = file.read()
                    print('Via flask',type(img))
                    prediction = predict_image(img)
                    with open('disease_dic.json') as json_file:
                        data = json.load(json_file)
            
                    print(data[prediction])      
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


@api.route('/fertilizer-predict')
class fertilizerPredict(Resource):
    def post(self):
        datas = json.loads(request.data)
        print(datas)
        crop_name = datas['cropname'].lower()
        N = datas['nitrogen']
        P = datas['phosphorous']
        K = datas['pottasium']
        # ph = float(request.form['ph'])

        df = pd.read_csv('models/Data/fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = float(nr) - float(N)
        p =float(pr) - float(P)
        k = float(kr) - float(K)
        
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"
        
        return {'fertilizer': str(fertilizer_dic[key]) }

    


                

        
        

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
   
