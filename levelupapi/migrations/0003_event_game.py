# Generated by Django 4.1.6 on 2023-02-08 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='levelupapi.game'),
            preserve_default=False,
        ),
    ]