print('hi')
import os
from flask import Flask
from flask.testing import FlaskClient
from config import app, db
import pytest


with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/fuel_guru_test.sql')), 'rb') as f:

    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app2():

    #conn = db.engine.connect()

    #trans = conn.begin()
    

    yield app

    #trans.rollback()
    #conn.close()


@pytest.fixture
def client():
    # set up before making requests. Recreate the db each time
    db.session.commit()
    db.drop_all()
    db.create_all()
    db.engine.execute(_data_sql)
    db.session.commit()
    
    yield app.test_client()
    
    db.session.close()
    db.session.remove()


@pytest.fixture
def runner():
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client: FlaskClient):
        self.client = client
        self.jwt = None

    def signin(self, iden='test', password='test'):
        resp = self.client.post(
            '/auth/signin',
            data={'iden': iden, 'password': password}
        )

        if resp.status_code == 200:
            self.jwt = resp.json.get('refresh_token')

        return resp

    def logout(self, jwt=None):
        return self.client.post('/auth/logout',
                                 headers={
                                     'Authorization': f'Bearer {jwt or self.jwt}'}
                                 )

@pytest.fixture
def auth(client:FlaskClient):
    return AuthActions(client)