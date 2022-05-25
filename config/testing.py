from flask_sqlalchemy import BaseQuery, Model, SQLAlchemy, SignallingSession
from sqlalchemy import orm

class TestSession(SignallingSession):    
    def commit(self):
        self.flush()
    
    def remove(self):
        self.expire_all()
        
        
class TestAlchemy(SQLAlchemy):
    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=Model,
                 engine_options=None):
        if app:
            self.app=app
        super().__init__(app, use_native_unicode, session_options, metadata, query_class, model_class, engine_options)
    
    def create_session(self, options):
        if self.app.config.get('TESTING'):
            return orm.sessionmaker(class_=TestSession, db=self, **options)
        else:
            return orm.sessionmaker(class_=SignallingSession, db=self, **options)