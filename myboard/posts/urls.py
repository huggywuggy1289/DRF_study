from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('post-form/', post_form_view, name='post-form'),  # 새로운 URL 패턴 추가
] + router.urls