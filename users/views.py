import requests, jwt

from django.views       import View
from django.http        import JsonResponse

from starfolio.settings import SECRET_KEY, ALGORITHM
from users.models       import User

class KakaoLogInView(View):
    def get(self, request):
        try:
            kakao_access_token  = request.headers.get('Authorization')
            kakao_user_info_api = 'https://kapi.kakao.com/v2/user/me'            
            user_info_response  = requests.get(kakao_user_info_api, headers={'Authorization' : f'Bearer {kakao_access_token}'}, timeout=2).json()
            
            kakao_id = user_info_response['id']
            name     = user_info_response['properties']['ninkname']
            email    = user_info_response['kakao_account']['email']
            
            user, is_created = User.objects.get_or_create(
                    kakao_id = kakao_id,
                    defaults={'name' : name, 'email' : email}
            )
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'message' : 'SUCCESS', 'access_token' : access_token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

