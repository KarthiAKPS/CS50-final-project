# Generated by Django 4.2.7 on 2023-12-25 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_spotifytoken_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spotifytoken',
            name='state',
        ),
    ]
