# Generated by Django 4.2.7 on 2023-12-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_user_access_token_remove_user_expires_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprivate',
            name='created_user',
            field=models.CharField(default='default', max_length=50, null=True, unique=True),
        ),
    ]
