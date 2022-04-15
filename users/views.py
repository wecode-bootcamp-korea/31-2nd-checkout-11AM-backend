import requests, jwt
from datetime    import datetime, timedelta

from django.shortcuts import redirect
from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

class GetUserInfoView(View):
    def get(self, request):
        try:
            code            = request.GET.get('code')
            kakao_token_api = 'https://kauth.kakao.com/oauth/token'
            data = {
                'grant_type': 'authorization_code',
                'client_id': settings.REST_API_KEY,
                'code': code
            }
            
            response       = requests.post(kakao_token_api, data = data, timeout = 3)   
            access_token   = response.json().get('access_token')
            kakao_user_api = 'https://kapi.kakao.com/v2/user/me'

            user_info = requests.get(kakao_user_api, headers = {'Authorization' : f'Bearer {access_token}'}, timeout = 3).json()
            
            if user_info.get('code') == -401:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
            
            kakao_id  = user_info['id']
            nickname  = user_info['properties']['nickname']
            email     = user_info['kakao_account']['email']

            user, created = User.objects.get_or_create(
                kakao_id = kakao_id, defaults = {'nickname' : nickname, 'email':email}
                )
            token = jwt.encode({'id' : user.id, 'iat' : datetime.utcnow(), 'exp':datetime.utcnow() + timedelta(days=2)}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({"token" : token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except requests.exceptions.Timeout:
            return JsonResponse({'message' : 'TIME_OUT_ERROR'}, status=408)