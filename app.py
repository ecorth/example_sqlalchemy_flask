from flask_jwt import JWT
from flask import Flask
from flask_restful import Api
from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity
from db import db

app = Flask(__name__)
db.init_app(app)
# no change structure of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run()
