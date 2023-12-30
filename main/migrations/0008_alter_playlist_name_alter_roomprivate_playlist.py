# Generated by Django 4.2.7 on 2023-12-22 04:36

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_playlist_playlist_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(default='default', max_length=255),
        ),
        migrations.AlterField(
            model_name='roomprivate',
            name='playlist',
            field=models.ForeignKey(default=main.models.get_default_playlist, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.playlist'),
        ),
    ]
