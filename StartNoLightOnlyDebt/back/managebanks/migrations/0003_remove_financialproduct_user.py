# Generated by Django 4.2.16 on 2024-11-18 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managebanks', '0002_alter_jeonseoption_dcls_month_creditloanoption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialproduct',
            name='user',
        ),
    ]
