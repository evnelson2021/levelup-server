# Generated by Django 4.1.6 on 2023-02-10 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_game_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='gamer',
            new_name='organizing_gamer',
        ),
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='levelupapi.game'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelupapi.event')),
                ('gamer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelupapi.gamer')),
            ],
        ),
    ]
