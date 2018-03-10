from db import db

class VoltageTypeModel(db.Model):
    __tablename__ = 'voltage_type'

    voltage_type_id = db.Column(db.Integer, primary_key=True)
    voltage_name = db.Column(db.String(80))

    def __init__(self, voltage_name):
        self.voltage_name = voltage_name

    def json(self):
        return {'voltage_type_id': self.voltage_type_id, 'voltage_name': self.voltage_name}

    @classmethod
    def find_by_name(cls, voltage_name):
        return cls.query.filter_by(voltage_name=voltage_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
