from datetime import date, datetime, timedelta
from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import desc, and_, select
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased


class GasStation(db.Model):
    __tablename__ = 'gas_stations'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    address = db.Column(db.String(255), nullable=False)

    lat = db.Column(db.Numeric, nullable=False)

    lng = db.Column(db.Numeric, nullable=False)

    image = db.Column(db.String())

    manager_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True)

    manager = db.relationship('User', backref='managed_gasstations')

    def __init__(self, name, address, lat, lng, image=None, manager=None, id=None):
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
        from model.posts import Post, PostType, Review
        
        p_type = PostType.query.filter_by(post_type_name='Review').first()

        q = GasStation.query.filter(GasStation.id == self.id)\
            .from_self(Review)\
            .join(GasStation.all_posts)\
            .filter(Post.post_type_id == p_type.id)\
            .where(Post.deleted_at==None)\
            .join(Review, and_(
                Review.post_id == Post.id,
                Review.last_edited == Post.last_edited))

        ratings = q.all()
        if len(ratings) > 1:
            vals = [rating.rating_val for rating in ratings]

            rating_only = sum(vals)

            num = (rating_only)/(len(vals))

        elif len(ratings) == 1:
            num = ratings[0].rating_val

        else:
            num = 0

        return num

    @hybrid_property
    def verified(self):
        return True if self.manager else False

    @hybrid_property
    def reviews(self):
        from model.posts import Post, PostType, Review
        
        today = datetime.fromisoformat(date.today().isoformat())

        this_week = today - timedelta(days=7)
        
        p_type = PostType.query.filter_by(post_type_name='Review').first()

        q = GasStation.query.filter(GasStation.id == self.id)\
            .from_self(Review)\
            .join(GasStation.all_posts)\
            .filter(Post.post_type_id == p_type.id)\
            .filter(Post.last_edited >= this_week)\
            .where(Post.deleted_at==None)\
            .join(Review, and_(
                Review.post_id == Post.id,
                Review.last_edited == Post.last_edited))

        return q.all()

    @hybrid_property
    def promotions(self):
        from model.posts import Post, Promotion
        
        today = datetime.fromisoformat(date.today().isoformat())
        
        q = GasStation.query.filter(GasStation.id == self.id)\
            .from_self(Promotion)\
            .join(GasStation.all_posts)\
            .where(Post.deleted_at==None)\
            .join(Promotion, and_(
                Promotion.post_id == Post.id,
                Promotion.last_edited == Post.last_edited))\
            .filter(Promotion.end_date >= today)\

        return q.all()

    @hybrid_property
    def amenities(self):
        """
        Gets all amenities posts for this gas station made in the last week
        """
        
        from model.posts import Post, AmenityTag
        
        q = GasStation.query.filter(GasStation.id == self.id)\
            .from_self(AmenityTag)\
            .join(GasStation.all_posts)\
            .where(Post.deleted_at==None)\
            .join(AmenityTag, and_(
                AmenityTag.post_id == Post.id,
                AmenityTag.last_edited == Post.last_edited))

        return q.all()

    @hybrid_property
    def gas_price_suggestions(self):
        from model.posts import GasPriceSuggestion, Post
        
        today = datetime.fromisoformat(date.today().isoformat())
        
        today = today - timedelta(days=1)

        q = GasStation.query.filter(GasStation.id == self.id)\
            .from_self(GasPriceSuggestion)\
            .join(GasStation.all_posts)\
            .where(Post.last_edited >= today)\
            .where(Post.deleted_at==None)\
            .join(GasPriceSuggestion, and_(
                GasPriceSuggestion.post_id == Post.id,
                GasPriceSuggestion.last_edited == Post.last_edited))

        return q.all()

    @hybrid_property
    def old_best_price(self):
        from model.posts import GasPriceSuggestion
        
        today = datetime.fromisoformat(date.today().isoformat())

        yesterday_start = today - timedelta(days=1, hours=12)
        
        return self._filter_date_and_votes(GasPriceSuggestion.last_edited.between(yesterday_start, today))

    @hybrid_property
    def current_best_price(self):
        from model.posts import GasPriceSuggestion
        
        today = datetime.fromisoformat(date.today().isoformat())  
        
        today = today - timedelta(days=1)
        
        return self._filter_date_and_votes(GasPriceSuggestion.last_edited >= today)


    def _filter_date_and_votes(self,cond):
        from model.posts import GasPriceSuggestion, Post, upvoted_posts, downvoted_posts, GasType, Gas
        
        dwn = aliased(
                select(
                    func.count(downvoted_posts.c.posts).label('downvs'),
                    downvoted_posts.c.posts.label('downid'))
                .where(
                    downvoted_posts.c.posts == Post.id)
                .group_by(downvoted_posts.c.posts).subquery(), name='downvote_count')

        upv = aliased(
            select(
                func.count(upvoted_posts.c.posts).label('upvs'),
                upvoted_posts.c.posts.label('upid'))
            .where(upvoted_posts.c.posts == Post.id)
            .group_by(upvoted_posts.c.posts).subquery(), name='upvote_count')

        net = aliased(select(
            (func.coalesce(upv.c.upvs, 0) -
                func.coalesce(dwn.c.downvs, 0)).label('net_v'),
            upv.c.upid.label('vid'))
            .select_from(
            dwn.join(upv, dwn.c.downid == upv.c.upid, full=True)).subquery(), name='net_votes')

        gas_types = GasType.query.all()
        res = []
        
        for gtype in gas_types:
            gas = GasStation.query.filter(GasStation.id == self.id)\
                .from_self(Gas)\
                .join(GasStation.all_posts)\
                .join(GasPriceSuggestion, and_(
                    GasPriceSuggestion.post_id == Post.id,
                    GasPriceSuggestion.last_edited == Post.last_edited))\
                .where(Post.deleted_at==None)\
                .join(Gas, GasPriceSuggestion.id==Gas.gas_post_id)\
                .filter(Gas.gas_type_id == gtype.id)\
                .join(net, net.c.vid == Post.id, full=True)\
                .filter(net.c.net_v >0)\
                .filter(cond)\
                .order_by(desc(net.c.net_v))\
                .order_by(desc(Post.last_edited))\
                .limit(1).first()
            if gas:
                res.append(gas)

        return res
        
