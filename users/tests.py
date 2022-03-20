import jwt

from django.test        import TestCase, Client
from unittest.mock      import MagicMock, patch

from .models            import User
from starfolio.settings import SECRET_KEY, ALGORITHM

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            id         = 1,
            name       = '박건규',
            password   = '',
            email      = '가짜이메일@가짜.com',
            kakao_id   = 1234567891111
        )

    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.views.requests')
    def test_success_to_login_when_kakao_token_exist_user(self, moked_requset):
        client       = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 1234567891111,
                    'kakao_account' : {
                        'email' : '가짜이메일@가짜.com'
                    },
                    'properties' : {
                        'nickname' : '박건규'
                    }
                }

        moked_requset.get = MagicMock(return_value = MockedResponse())
        headers           = {'HTTP_Authorization' : 'fake_token'}
        response          = client.get("/users/kakao-login", **headers)

        self.assertEqual(response.status_code, 200)
    
    @patch('users.views.requests')
    def test_success_to_login_when_kakao_token_new_user(self, moked_requset):
        client       = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id' : 15155151515,
                    'kakao_account' : {
                        'email' : '가짜이메일2@가짜2.com'
                    },
                    'properties' : {
                        'nickname' : '가짜박건규'
                    }
                }
        
        moked_requset.get = MagicMock(return_value = MockedResponse())
        headers           = {'HTTP_Authorization' : 'fake_kkkktoken'}
        response          = client.get("/users/kakao-login", **headers)

        self.assertEqual(response.status_code, 200)

    @patch('users.views.requests')
    def test_fail_to_login_when_invalid_token_in_headers(self, moked_requset):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'code' : -401
                }
        
        moked_requset.get = MagicMock(return_value = MockedResponse())
        headers           = {'HTTP_Authorization' : 'invalidtoken123123'}
        response          = client.get("/users/kakao-login", headers)

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.json(),
            {
                'message' : 'INVALID_TOKEN'
            }
        )

    @patch('users.views.requests')
    def test_fail_to_login_when_invalid_response_in_kakao(self, moked_requset):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id' : 15155151515,
                    'properties' : {
                        'nickname' : '가짜박건규'
                    }
                }
        
        moked_requset.get = MagicMock(return_value = MockedResponse())
        headers           = {'HTTP_Authorization' : 'invalidtoken123123'}
        response          = client.get("/users/kakao-login", headers)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )
