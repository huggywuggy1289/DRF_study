from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile
# user = User.objects.get(pk=1)
# posts = user.posts.all()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') #router.register
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    body = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.png')
    likes = models.ManyToManyField(User, related_name = 'like_posts', blank=True) 
    # author과 user이 전부 User 모델을 참고하고 있어서 에러가 발생함. 이럴경우 한쪽에
    # 꼭 related_name을 지정해야함.
    published_date = models.DateTimeField(default=timezone.now)

#댓글모델(author, profile, post, text)
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) #router.register
    text = models.TextField()
