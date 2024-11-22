from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 사용
from managebanks.models import JeonseOption, CreditLoanOption, MortgageOption


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interaction_likes"  # 고유한 related_name 설정
    )
    jeonse_option = models.ForeignKey(
        JeonseOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="jeonse_likes"
    )
    credit_loan_option = models.ForeignKey(
        CreditLoanOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="credit_likes"
    )
    mortgage_option = models.ForeignKey(
        MortgageOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mortgage_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("user", "jeonse_option"),
            ("user", "credit_loan_option"),
            ("user", "mortgage_option"),
        )


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interaction_comments'  # related_name을 interaction_comments로 설정
    )
    jeonse_option = models.ForeignKey(
        JeonseOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )
    credit_loan_option = models.ForeignKey(
        CreditLoanOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )
    mortgage_option = models.ForeignKey(
        MortgageOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]
