# Generated by Django 4.1.4 on 2022-12-18 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_cell_arena_cell_surface_type_character_playable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='image',
            field=models.ImageField(null=True, upload_to='game/image/'),
        ),
    ]
