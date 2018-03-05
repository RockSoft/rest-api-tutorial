import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.voltage_type import VoltageType, VoltageTypeList

app = Flask(__name__)
print("This is my database url: %s" % os.environ(DATABASE_URL))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'peter'
api = Api(app)


jwt = JWT(app, authenticate, identity_function) #/auth

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(VoltageType, '/voltagetype/<string:voltage_name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(VoltageTypeList, '/voltagetypes')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
