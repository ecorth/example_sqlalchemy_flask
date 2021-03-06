from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # data = request.get_json(force=True) force=True means that you no need content header
    # data = request.get_json(silent=True) silent=True is doesn't give error return none

    def post(self, name):
        """
        item = {'name': name, 'price': 12.00}
        :param name:
        :return:
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        item = ItemModel(name, data['price'])
        item.save_to_db()
        return {"item": item.json()}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db(item)

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
