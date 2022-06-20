import pytest

from tests.conftest import AuthActions


class TestAdmin():
    url = '/admin'

    @pytest.mark.parametrize(
        ('iden', 'password', 'firstname', 'lastname', 'email', 'code'), [
            pytest.param('robertwallace', '5oORdvjq*t4K', 'Gianna',
                         'Rhodes', 'fuelguru.app@gmail.com', 200, id='UT70'),
            pytest.param('marckennedy', 'ZBly62WopR$2', 'Gianna',
                         'Rhodes', 'fuelguru.app@gmail.com', 403, id='UT71')
        ]
    )
    def test_add_gas_station_manager(self, auth: AuthActions, iden, password, firstname, lastname, email, code):
        auth.signin(iden, password)

        body = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        }

        resp = auth.client.post(f'{self.url}/gasstations/manager', data=body, headers={
            'Authorization': f'Bearer {auth.jwt}'})

        resp.status_code == code
