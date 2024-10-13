from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('post-form/', post_form_view, name='post-form'),  # 새로운 URL 패턴 추가
    path('like/<int:pk>/', like_post, name = 'like_post'),
] + router.urls