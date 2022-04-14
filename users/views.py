import requests, jwt
from datetime    import datetime, timedelta

from django.shortcuts import redirect
from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

class GetUserInfoView(View):
    
    def request_access_token(self, auth_code):
        try:
            kakao_auth_url = 'https://kauth.kakao.com/oauth/token'
            data = {
                    'grant_type': 'authorization_code',
                    'client_id' : settings.KAKAO_REST_API_KEY,
                    'code'      : auth_code
                    }
            response       = requests.post(kakao_auth_url, data = data, timeout = 3)   
            access_token   = response.json().get('access_token')
            
            return access_token
    
        except requests.exceptions.Timeout:
            return JsonResponse({'message' : 'TIME_OUT_ERROR'}, status=408)        
    
    def request_user_data(self, access_token):
        try:
            kakao_user_api = 'https://kapi.kakao.com/v2/user/me'
            user_info      = requests.get(kakao_user_api, headers = {'Authorization' : f'Bearer {access_token}'}, timeout = 3).json()
            
            if user_info.get('code') == -401:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
            
            return user_info
        
        except requests.exceptions.Timeout:
            return JsonResponse({'message' : 'TIME_OUT_ERROR'}, status=408)
    
    def create_user(self, user_info):
        kakao_id  = user_info['id']
        nickname  = user_info['properties']['nickname']
        email     = user_info['kakao_account']['email']

        user, created = User.objects.get_or_create(
            kakao_id = kakao_id, defaults = {'nickname' : nickname, 'email':email}
            )
        
        return user
    
    def publish_token(self, user):
        token = jwt.encode({'id' : user.id, 'iat' : datetime.utcnow(), 'exp':datetime.utcnow() + timedelta(days=2)}, settings.SECRET_KEY, settings.ALGORITHM)
        
        return token
    
    def get(self, request):
        try:
            code = request.GET.get('code')
            
            access_token = self.request_access_token(code)
            user_data    = self.request_user_data(access_token)
            user         = self.create_user(user_data)
            token        = self.publish_token(user)
            
            return JsonResponse({"token" : token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)