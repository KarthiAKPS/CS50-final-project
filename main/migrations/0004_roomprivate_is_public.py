# Generated by Django 4.2.7 on 2023-12-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_user_spotify_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomprivate',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]