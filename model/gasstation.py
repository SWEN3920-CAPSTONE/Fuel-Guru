from config import db
from sqlalchemy.ext.hybrid import hybrid_property

from model.posts import Post, Rating, Review


class GasStation(db.Model):
    __tablename__ = 'gas_stations'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    address = db.Column(db.String(255), nullable=False)

    lat = db.Column(db.Numeric, nullable=False)

    lng = db.Column(db.Numeric, nullable=False)

    image = db.Column(db.LargeBinary)

    manager_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True)

    posts = db.relationship(
        'Post', backref='gas_station', cascade='all, delete')

    manager = db.relationship('User', backref='managed_gasstations')

    def __init__(self, name, address, lat, lng, image, manager=None, id=None):
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng
        self.image = image
        self.manager = manager
        self.id = id

    def __repr__(self) -> str:
        return f'{self.name} with manager {self.manager}'

    # derived attributes

    @hybrid_property
    def avg_rating(self):
        rating = None

    @hybrid_property
    def verified(self):
        return True if self.manager else False
