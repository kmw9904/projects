from django.db import models
from django.conf import settings

# 개인대출 좋아요 관리
class CreditComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_comments')
    product = models.ForeignKey('managebanks.CreditLoanOption', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.product}"

class CreditLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_likes')
    product = models.ForeignKey('managebanks.CreditLoanOption', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 한 사용자가 한 상품에 한 번만 좋아요 가능

    def __str__(self):
        return f"Like by {self.user} on {self.product}"

# 전세대출 좋아요 관리
class JeonseComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jeonse_comments')
    product = models.ForeignKey('managebanks.JeonseOption', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.product}"

class JeonseLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jeonse_likes')
    product = models.ForeignKey('managebanks.JeonseOption', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Like by {self.user} on {self.product}"


# 담보대출 좋아요 관리
class MortgageComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mortgage_comments')
    product = models.ForeignKey('managebanks.MortgageOption', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.product}"

class MortgageLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mortgage_likes')
    product = models.ForeignKey('managebanks.MortgageOption', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Like by {self.user} on {self.product}"