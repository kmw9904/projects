# Generated by Django 4.2.16 on 2024-11-24 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managebanks', '0001_initial'),
        ('interactions', '0002_comment_like_alter_creditlike_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='credit_loan_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_likes', to='managebanks.creditloanoption'),
        ),
        migrations.AlterField(
            model_name='like',
            name='jeonse_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jeonse_likes', to='managebanks.jeonseoption'),
        ),
        migrations.AlterField(
            model_name='like',
            name='mortgage_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mortgage_likes', to='managebanks.mortgageoption'),
        ),
    ]
