import pytest
from flask.testing import FlaskClient

from tests.conftest import AuthActions
from tests.utils import (has_incorrect_user_cred_error,
                         has_invalid_email_error, has_invalid_firstname_error,
                         has_invalid_lastname_error, has_invalid_token_error,
                         has_logout_success, has_pwd_form_error,
                         has_pwd_length_error, has_refresh_token,
                         has_used_email_error, has_used_username_error,
                         has_user_deleted_error, has_username_form_error,
                         has_username_length_error)


class TestAuth():
    url = '/auth'

    @pytest.mark.parametrize(
        ('firstname', 'lastname', 'username', 'email', 'password', 'code', 'func'), [
            pytest.param('Mike', 'Henry', 'MikeH123', 'MikeHenry@gmail.com',
                         'T3$tData1234', 200, lambda resp: has_refresh_token(resp), id='UT2'),
            pytest.param('Mike', 'Henry', 'MikeH123', 'MikeHenry@gmail.com',
                         'T3$tData12', 400, lambda resp: has_pwd_length_error(resp), id='UT5'),
            pytest.param('Mike', 'Henry', 'MikeH123', 'MikeHenry@gmail.com', 'TestData123', 400,
                         lambda resp: has_pwd_length_error(resp) or has_pwd_form_error(resp), id='UT7'),
            pytest.param('Mike123', 'Henry', 'MikeH123', 'MikeHenry@gmail.com', 'T3$tData1234',
                         400, lambda resp: has_invalid_firstname_error(resp), id='UT9'),
            pytest.param('Mike', 'Henry#', 'MikeH123', 'MikeHenry@gmail.com', 'T3$tData1234',
                         400, lambda resp: has_invalid_lastname_error(resp),  id='UT11'),
            pytest.param('Mike', 'Henry', 'MikeH123', 'MikeHenrygmail.com', 'T3$tData1234',
                         400, lambda resp: has_invalid_email_error(resp), id='UT13'),
            pytest.param('Mike', 'Henry', 'M!keH123', 'MikeHenry@gmail.com', 'T3$tData1234',
                         400, lambda resp: has_username_form_error(resp), id='UT15'),
            pytest.param('Mike', 'Henry', 'Mike', 'MikeHenry@gmail.com', 'T3$tData1234',
                         400, lambda resp: has_username_length_error(resp), id='UT17'),
            pytest.param('Mike', 'Henry', 'MikeHenry_Test1234567890DataTooLong', 'MikeHenry@gmail.com',
                         'T3$tData1234', 400, lambda resp: has_username_length_error(resp), id='UT19'),
            pytest.param('Mike', 'Henry', 'marckennedy', 'MikeHenry@gmail.com',
                         'T3$tData1234', 409, lambda resp: has_used_username_error(resp), id='UT20'),
            pytest.param('Mike', 'Henry', 'MikeH123', 'daviesoscar@example.org',
                         'T3$tData1234', 409, lambda resp: has_used_email_error(resp), id='UT21')
        ]
    )
    def test_signup(self, client: FlaskClient, firstname, lastname, username, email, password, code, func):
        body = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': password
        }

        response = client.post(f'{self.url}/signup', data=body)
        assert response.status_code == code
        func(response)

    @pytest.mark.parametrize(
        ('iden', 'password', 'code', 'func'),
        [
            pytest.param('daviesoscar@example.org', '#o35Pu@P7KMx',
                         200, lambda resp: has_refresh_token(resp), id='UT22'),
            pytest.param('marckennedy', 'ZBly62WopR$2', 200,
                         lambda resp: has_refresh_token(resp), id='UT23'),
            pytest.param('ThisaccountdoesnotExist', 'T3$tData1234', 401,
                         lambda resp: has_incorrect_user_cred_error(resp), id='UT24'),
            pytest.param('kgarcia', 'T3$tData1234', 401,
                         lambda resp: has_incorrect_user_cred_error(resp), id='UT25'),
            pytest.param('marckennedy', 'T3$tData12', 400,
                         lambda resp: has_pwd_length_error(resp), id='UT26'),
            pytest.param('marckennedy', 'Testdata1234', 400,
                         lambda resp: has_pwd_form_error(resp), id='UT27'),
            pytest.param('dawn21', '@(FJw64bLn5Z', 401,
                         lambda resp: has_user_deleted_error(resp), id='UT28')
        ]
    )
    def test_signin(self, client: FlaskClient, iden, password, code, func):
        body = {
            'iden': iden,
            'password': password
        }

        response = client.post(f'{self.url}/signin', data=body)
        assert response.status_code == code
        func(response)

    @pytest.mark.parametrize(
        ('iden', 'password', 'twice', 'jwt', 'code', 'func'),
        [
            pytest.param('marckennedy', 'ZBly62WopR$2', False, None,
                         200, lambda resp: has_logout_success(resp), id='UT29'),
            pytest.param('marckennedy', 'ZBly62WopR$2', True, None, 200,
                         lambda resp: has_invalid_token_error(resp), id='UT30'),
            pytest.param(None, None, False, None, 401,
                         lambda resp: has_invalid_token_error(resp), id='UT31'),
            pytest.param(None, None, False, 'Hi', 401,
                         lambda resp: has_invalid_token_error(resp), id='UT32')
        ]
    )
    def test_logout(self, auth: AuthActions, iden, password, twice, jwt, code, func):

        auth.signin(iden, password)

        res = auth.logout(jwt)

        assert res.status_code == code

        if twice:
            res = auth.logout(jwt)

            assert res.status_code == 400

        func(res)
