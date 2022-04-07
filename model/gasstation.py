from config import db

class GasStation(db.Model):
    __tablename__ = 'gas_stations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    lat =  db.Column(db.Numeric, nullable=False)
    lng = db.Column(db.Numeric, nullable=False)
    image = db.Column(db.String(255))
    
    manager_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=True)
    
    def __init__(self, id, name, address, lat, lng, image,manager_id):
        self.id = id
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng
        self.image = image
        self.manager_id = manager_id
    