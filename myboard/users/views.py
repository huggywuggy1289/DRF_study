from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer # 회원가입 시리얼라이저의 클래스명

# view is mostly simple because serializer code.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() # 기본적으로 유저 쿼리셋 가져오고
    serializer_class = RegisterSerializer # 시리얼라이저 등록하는 형식이 views의 기본이 된다.
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # 토큰 받아오기
        return Response({"token" : token.key}, status=status.HTTP_200_OK)



