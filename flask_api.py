from flask import Flask , jsonify
from flask_restx import Resource, Api
from newsscrapper import scraper

app = Flask(__name__)
api = Api(app)

@api.route('/news')
class HelloWorld(Resource):
    def get(self):
        return jsonify(scraper())

if __name__ == '__main__':
    app.run(debug=True)