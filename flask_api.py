from flask import Flask , jsonify
from flask_restx import Resource, Api
from newsscrapper import scraper
import os

app = Flask(__name__)
api = Api(app)

@api.route('/news')
class HelloWorld(Resource):
    def get(self):
        return jsonify(scraper())

@api.route('/')
class home(Resource):
    def get(self):
        return {'hello':'world'}

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)