from flask_restful import Resource
from models.voltage_type import VoltageTypeModel

class VoltageType(Resource):

    def get(self, voltage_name):
        voltage_type = VoltageTypeModel.find_by_name(voltage_name)

        if voltage_type:
            return voltage_type.json()
        return {'message': 'Voltage type not found'}, 404

    def post(self, voltage_name):
        if VoltageTypeModel.find_by_name(voltage_name):
            return {'message': "Voltage type with name '{}' already exists".format(voltage_name)},400

        voltage_type = VoltageTypeModel(voltage_name)
        try:
            voltage_type.save_to_db()
        except:
            return {'message': 'An error occurred while creating the voltage type.'}, 500

        return voltage_type.json(), 201

    def delete(self, voltage_name):
        voltage_type = VoltageTypeModel.find_by_name(voltage_name)
        if voltage_type:
            voltage_type.delete_from_db()

        return {'message': 'voltage type deleted'}


class VoltageTypeList(Resource):
    def get(self):
        return {'voltagetypes': [voltagetype.json() for voltagetype in VoltageTypeModel.query.all()]}
