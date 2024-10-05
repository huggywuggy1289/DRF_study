from rest_framework import serializers

from users.serializers import ProfileSerializer #users앱의 시리얼라이저 명칭
from .models import *

# 알아서 채워져야하는 유저 정보
class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "likes")

# 게시글 작성
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "category", "body", "image")