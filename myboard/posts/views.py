from django.shortcuts import render
from rest_framework import viewsets
from users.models import Profile
from .permissions import CustomReadOnly
from .serializers import *
from .models import Post
# +
from rest_framework.exceptions import NotAuthenticated

from django_filters.rest_framework import DjangoFilterBackend # view마다 필터설정할 필요없음.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permmision_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'likes']

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PostSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        # 인증되지 않은 사용자는 예외를 발생시킴(Field 'id' expected a number but got anomyous user 에러..)
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("이 작업을 수행하기 위해서는 인증된 사용자여야만 합니다.")
        
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)

# https://kgw08003.tistory.com/60

# posts.html 템플릿을 렌더링할 수 있는 뷰를 추가(api만 조회하는 대신 직접 템플릿으로 조회)
def post_form_view(request):
    return render(request, 'posts/posts.html')