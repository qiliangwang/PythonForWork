import json
from flask import Flask
import flask_restful as restful

app = Flask(__name__)
api = restful.Api(app)

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

seller = data['seller']
goods = data['goods']
ratings = data['ratings']


class Seller(restful.Resource):
    def get(self):
        return {'error': 0,
                'data': seller,
                }


class Goods(restful.Resource):
    def get(self):
        return {'error': 0,
                'data': goods,
                }


class Ratings(restful.Resource):
    def get(self):
        return {'error': 0,
                'data': seller,
                }


api.add_resource(Seller, '/api/seller')
api.add_resource(Goods, '/api/goods')
api.add_resource(Ratings, '/api/ratings')


if __name__ == '__main__':
    app.run(debug=True)
