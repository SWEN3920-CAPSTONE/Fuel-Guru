import base64
import itertools
from pprint import pprint
from faker import Faker
import pytest
from flask.testing import FlaskClient

from tests.conftest import AuthActions
from tests.utils import has_date_range_error, has_disallowed_post_type_error, has_duplicate_gas_type_error, has_invalid_date_error, has_invalid_num_error, has_invalid_token_error, has_length_range_error, has_manager_post_error, has_min_value_error, has_post_created, has_value_range_error

fake = Faker()

class TestPosts():
    url = '/posts'
    
    @pytest.mark.parametrize(
        ('iden','password','body', 'code', 'func'),
        [
            pytest.param('marckennedy', 'ZBly62WopR$2', 'This gas station has food',200,lambda resp: has_post_created(b'Comment', resp) , id='UT34'),
            pytest.param('marckennedy', 'ZBly62WopR$2','', 400,lambda resp: has_length_range_error(resp), id='UT36'),
            pytest.param('marckennedy', 'ZBly62WopR$2','I', 200,lambda resp: has_post_created(b'Comment', resp), id='UT38'),
            pytest.param('marckennedy', 'ZBly62WopR$2', fake.pystr(min_chars=501,max_chars=501), 400,lambda resp: has_length_range_error(resp), id='UT40'),
            pytest.param('kgarcia', 'vYMovXVs^58Q','comment',403, lambda resp: has_disallowed_post_type_error(b'Comment', resp), id='UT41'),
            pytest.param(None,None,'comment', 401, lambda resp: has_invalid_token_error(resp), id='UT42'),            
        ]
    )
    def test_create_comment(self,auth:AuthActions,iden,password,body,code, func):
        auth.signin(iden,password)
        
        data = {
            'gas_station_id':1,
            'post_type_id':1,
            'comment': {
                'body':body
            }
        }
        
        resp = auth.client.post(f'{self.url}', json=data, headers={
                                     'Authorization': f'Bearer {auth.jwt}'})
        
        assert resp.status_code == code
        func(resp)
        
    
    @pytest.mark.parametrize(
        ('iden','password','rating_val', 'code', 'func'),
        [
            pytest.param('marckennedy', 'ZBly62WopR$2', 1,200,lambda resp: has_post_created(b'Rating', resp) , id='UT44'),
            pytest.param('marckennedy', 'ZBly62WopR$2',5, 200,lambda resp: has_post_created(b'Rating', resp) , id='UT46'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',3,403, lambda resp: has_disallowed_post_type_error(b'Rating', resp), id='UT47'),
            pytest.param('marckennedy', 'ZBly62WopR$2', 0, 400,lambda resp: has_value_range_error(resp), id='UT48'),
            pytest.param('marckennedy', 'ZBly62WopR$2', 6, 400,lambda resp: has_value_range_error(resp), id='UT49'),
            pytest.param(None,None, 2, 401, lambda resp: has_invalid_token_error(resp), id='UT50')         
        ]
    )
    def test_create_rating(self,auth:AuthActions,iden,password,rating_val,code,func):
        auth.signin(iden,password)
        
        data = {
            'gas_station_id':1,
            'post_type_id': 2,
            'rating': {
                'rating_val': rating_val
            }
        }
        
        resp = auth.client.post(f'{self.url}', json=data, headers={
            'Authorization': f'Bearer {auth.jwt}'})
        assert resp.status_code == code
        func(resp)
        
    
    @pytest.mark.parametrize(
        ('body', 'code', 'func'),
        [
            pytest.param('This gas station has food',200,lambda resp: has_post_created(b'Review', resp)),
            pytest.param('', 400,lambda resp: has_length_range_error(resp)),
            pytest.param('I', 200,lambda resp: has_post_created(b'Review', resp)),
            pytest.param(fake.pystr(min_chars=501,max_chars=501), 400,lambda resp: has_length_range_error(resp))           
        ],
        ids=itertools.count(1)
    )
    @pytest.mark.parametrize(
        ('iden','password','rating_val', 'code2', 'func2'),
        [
            pytest.param('marckennedy', 'ZBly62WopR$2', 1,200,lambda resp: has_post_created(b'Review', resp), id='UT51' ),
            pytest.param('marckennedy', 'ZBly62WopR$2',5, 200,lambda resp: has_post_created(b'Review', resp), id='UT52' ),
            pytest.param('kgarcia', 'vYMovXVs^58Q',3,403, lambda resp: has_disallowed_post_type_error(b'Review', resp), id='UT53' ),
            pytest.param('marckennedy', 'ZBly62WopR$2', 0, 400,lambda resp: has_value_range_error(resp), id='UT54' ),
            pytest.param('marckennedy', 'ZBly62WopR$2', 6, 400,lambda resp: has_value_range_error(resp), id='UT55' ),
            pytest.param(None,None, 2, 401, lambda resp: has_invalid_token_error(resp), id='UT56')         
        ]
    )  
    def test_create_review(self, auth:AuthActions, iden, password, rating_val, body, code, func, code2, func2):
        auth.signin(iden,password)
        
        data = {
            'gas_station_id':1,
            'post_type_id': 3,
            'review': {
                'rating_val': rating_val,
                'body':body
            }
        }
        
        resp = auth.client.post(f'{self.url}', json=data, headers={
            'Authorization': f'Bearer {auth.jwt}'})
        
        if code == code2:
        
            assert resp.status_code == code
        
            func(resp)
            func2(resp)
            
        if code2 == 401:
            assert resp.status_code == code2
            
            func2(resp)
            return
            
        if code2 == 400 and code != 400:
            assert resp.status_code == code2
            
            func2(resp)
            return
            
        if code == 400 and code2 != 400:
            assert resp.status_code == code
            
            func(resp)
            return
            
        if code2 == 403:
            assert resp.status_code == code2
            
            func2(resp)
            return
            
            
    @pytest.mark.parametrize(
        ('iden', 'password','gas_station_id', 'start_date', 'end_date', 'desc', 'image', 'code', 'func'),
        [
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,'2022-05-22T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', base64.b64encode(fake.image()).decode('utf-8'), 200, lambda resp: has_post_created(b'Promotion', resp), id='UT57'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',1,'2022-05-22T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', base64.b64encode(fake.image()).decode('utf-8'), 403, lambda resp: has_manager_post_error(resp), id='UT58'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,'05-2022-22T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', None, 400, lambda resp: has_invalid_date_error(resp), id='UT59'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,'2022-02-29T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', None, 400, lambda resp: has_invalid_date_error(resp), id='UT60'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,'2022-06-24T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', None, 400, lambda resp: has_date_range_error(resp), id='UT61'),
            pytest.param('marckennedy', 'ZBly62WopR$2',2,'2022-03-22T00:00:00Z','2022-05-22T00:00:00Z','We are having a sale', None, 403, lambda resp: has_disallowed_post_type_error(b'Promotion', resp), id='UT62'),
        ]
    )
    def test_create_promotion(self, auth:AuthActions, iden, password,gas_station_id, start_date, end_date, desc, image, code, func):
        auth.signin(iden,password)
        
        data = {
            'gas_station_id':gas_station_id,
            'post_type_id': 4,
            'promotion': {
                'desc': desc,
                'start_date': start_date,
                'end_date': end_date,
                'image': image
            }
        }
        
        resp = auth.client.post(f'{self.url}', json=data, headers={
            'Authorization': f'Bearer {auth.jwt}'})
        
        assert resp.status_code == code
        
        func(resp)
        
        
    @pytest.mark.parametrize(
        ('iden','password','gas_station_id','gases','code','func'),
        [
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,[{'gas_type_id':1, 'price':90}, {'gas_type_id':2, 'price':70}],200,lambda resp: has_post_created(b'Gas Price Suggestion', resp), id='UT63'),
            pytest.param('marckennedy', 'ZBly62WopR$2', 1,[{'gas_type_id':1, 'price':93}],200,lambda resp: has_post_created(b'Gas Price Suggestion', resp), id ='UT64'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,[{'gas_type_id':1, 'price':-90}],400,lambda resp: has_min_value_error(resp), id='UT65'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,[{'gas_type_id':1, 'price':90}, {'gas_type_id':1, 'price':70}],400,lambda resp: has_duplicate_gas_type_error(resp), id='UT66'),
            pytest.param('kgarcia', 'vYMovXVs^58Q',2,[{'gas_type_id':1, 'price':90}, {'gas_type_id':2, 'price': 'sevent@y'}],400,lambda resp: has_invalid_num_error(resp), id='UT67')       
        ]
    )
    def test_gas_price_suggestion(self, auth:AuthActions, iden, password, gas_station_id, gases, code, func):
        
        auth.signin(iden,password)
    
        data = {
            'gas_station_id':gas_station_id,
            'post_type_id': 5,
            'gas_price_suggestion': {
                'gases': gases
            }
        }
        
        resp = auth.client.post(f'{self.url}', json=data, headers={
            'Authorization': f'Bearer {auth.jwt}'})
        print(resp.data)
        assert resp.status_code == code
        
        func(resp)