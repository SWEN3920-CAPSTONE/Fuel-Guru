from flask.testing import FlaskClient
import pytest

from tests.conftest import AuthActions


class TestUsers():
    url = '/users'

    @pytest.mark.parametrize(
        ('iden', 'password', 'code'), [
            pytest.param('marckennedy', 'ZBly62WopR$2', 200, id='UT58'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', 200, id='UT59'),
            pytest.param('dawn21', '@(FJw64bLn5Z', 401, id='UT60'),
        ]
    )
    def test_user_profile(self, auth: AuthActions, iden, password, code):

        response = auth.signin(iden, password)
        response.status_code == code

        response = auth.client.get(f'{self.url}', headers={
            'Authorization': f'Bearer {auth.jwt}'})
        response.status_code == code

    @pytest.mark.parametrize(
        ('iden', 'password', 'data', 'code'), [
            pytest.param('marckennedy', 'ZBly62WopR$2', {
                         'current_email': 'stephenhanson@example.com', 'new_email': 'marky@gmail.com'}, 200, id='UT61'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', {
                         'firstname': 'Stacy'}, 200, id='UT62'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', {
                         'lastname': 'Stacy'}, 200, id='UT63'),
            pytest.param('marckennedy', 'ZBly62WopR$2', {
                         'current_password': 'ZBly62WopR$2', 'new_password': 'Testing123@$'}, 200, id='UT64'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', {
                         'current_password': 'vYMovXVs^58Q767454', 'new_password': 'Testing123@$'}, 403, id='UT65'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', {
                         'current_email': 'p67aulvaughn@example.org', 'new_email': 'markyg@gmail.com'}, 403, id='UT66'),
            pytest.param('marckennedy', 'ZBly62WopR$2', {
                         'current_email': 'stephenhanson@example.com', 'new_email': 'paulvaughn@example.org'}, 409, id='UT67'),
        ]
    )
    def test_edit_user(self, auth: AuthActions, iden, password, data, code):
        auth.signin(iden, password)

        response = auth.client.put(f'{self.url}', data=data, headers={
            'Authorization': f'Bearer {auth.jwt}'})
        response.status_code == code

    @pytest.mark.parametrize(
        ('iden', 'password', 'code'), [
            pytest.param('marckennedy', 'ZBly62WopR$2', 200, id='UT68'),
            pytest.param('kgarcia', 'vYMovXVs^58Q', 200, id='UT69'),
        ]
    )
    def test_delete_user(self, auth: AuthActions, iden, password, code):

        response = auth.signin(iden, password)
        response.status_code == code

        response = auth.client.delete(f'{self.url}', headers={
            'Authorization': f'Bearer {auth.jwt}'})
        response.status_code == code
        
        
    