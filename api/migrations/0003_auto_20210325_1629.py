# Generated by Django 3.1.7 on 2021-03-25 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210325_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avg_score_social',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avg_score_social', to='api.score'),
        ),
        migrations.AddField(
            model_name='user',
            name='avg_score_tech',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avg_score_tech', to='api.score'),
        ),
    ]
