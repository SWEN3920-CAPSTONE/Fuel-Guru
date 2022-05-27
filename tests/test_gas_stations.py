import pytest
from faker import Faker
from flask.testing import FlaskClient
fake = Faker()


class TestGasStations():
    url = '/gasstations'

    @pytest.mark.parametrize(
        ('name', 'cheapest', 'code'),
        [
            pytest.param('W', False, 200, id='UT76'),
            pytest.param('W', True, 404, id='UT77'),
            pytest.param('Wpouk', False, 404, id='UT78'),
        ]
    )
    def test_search(self, client: FlaskClient, name, cheapest, code):
        body = {
            'name': name,
            'cheapest': cheapest
        }

        resp = client.post(f'{self.url}/search', data=body)
        print(resp.data)
        assert resp.status_code == code

    @pytest.mark.parametrize(
        ('gid', 'code'),
        [
            pytest.param(1, 200, id='UT79'),
            pytest.param('Hi', 404, id='UT80'),
            pytest.param(0, 404, id='UT81')
        ]
    )
    def test_get_gasstation(self, client: FlaskClient, gid, code):

        resp = client.get(f'{self.url}/{gid}')
        print(resp.data)

        assert resp.status_code == code
