from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from users.models import Profile
from .permissions import CustomReadOnly
from .serializers import *
from .models import Post

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# +
from rest_framework.exceptions import NotAuthenticated

from django_filters.rest_framework import DjangoFilterBackend # view마다 필터설정할 필요없음.

# class로 뷰함수 처리를 하는 경우는 router로 url등록을 한다.

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

# 좋아요 기능
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return Response({'status':'ok'})

# 댓글 기능
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [CustomReadOnly]  # 여기에서 'permmision'을 'permission'으로 수정

    def get_serializer_class(self):  # list(목록 조회), retrieve(단일 항목 조회)
        if self.action in ['list', 'retrieve']:
            return CommentSerializer  # 이 경우는 댓글목록이나 특정 댓글 조회할때 사용
        return CommentCreateSerializer  # 조회가 이닌경우는 댓글 작성에 속함.
    
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)

