# Generated by Django 4.1.4 on 2022-12-18 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_cell_bagitem_arena'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='arena',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='game.arena'),
        ),
        migrations.AddField(
            model_name='cell',
            name='surface_type',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='playable',
            field=models.BooleanField(null=True),
        ),
        migrations.CreateModel(
            name='SpecialMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='game.character')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='game.event')),
            ],
            options={
                'db_table': '"game"."special_move"',
                'managed': True,
            },
        ),
    ]
