from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 사용

class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 사용자 모델 참조
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_articles',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 사용자 모델 참조
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]
