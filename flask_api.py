from flask import Flask , jsonify,request,Markup
import json
from flask_restx import Resource, Api
from newsscrapper import scraper
from werkzeug.utils import secure_filename
from disease_predictions import predict_image
from utils.disease import disease_dic
import os




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
                

        
        

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)