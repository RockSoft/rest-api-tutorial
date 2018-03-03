from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.voltage_type import VoltageTypeModel

class VoltageType(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        voltage_type = VoltageTypeModel.find_by_name(name)
        if voltage_type:
            return voltage_type.json()
        return {'message':'voltage_type not found'}, 404

    def post(self, name):
        if VoltageTypeModel.find_by_name(name):
            return {"message": "A a voltage_type with name '{}' already exists".format(name)}, 400

        voltage_type = VoltageTypeModel(name)
        try:
            voltage_type.save_to_db()
        except:
            return {'message': 'An error occurred inserting the voltage_type'}, 500 #internal server error

        return voltage_type.json(), 201

    def delete(self, name):
        voltage_type = VoltageTypeModel.find_by_name(name)
        if voltage_type:
            voltage_type.delete_from_db()

        return {'message': 'Voltage Type deleted'}

    def put(self, name):
        data = VoltageType.parser.parse_args()

        # We first see if the the item already exists by name
        voltage_type = VoltageTypeModel.find_by_name(name)

        if voltage_type is None:
            # Item doesn't exist so we create a new object
            voltage_type = VoltageTypeModel(name, **data)
        else:
            # item does exist so we just need to update the price & the store id
            voltage_type.name = data['name']

        # The save_to_db() will then either insert or update the database
        voltage_type.save_to_db()

        return voltage_type.json()


class VoltageTypeList(Resource):
    def get(self):
        return {'Voltage Types': [voltage_type.json() for voltage_type in VoltageTypeModel.query.all()]}
