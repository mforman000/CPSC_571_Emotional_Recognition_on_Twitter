# Generated by Django 5.0.3 on 2024-04-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TweetRecognitionApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
