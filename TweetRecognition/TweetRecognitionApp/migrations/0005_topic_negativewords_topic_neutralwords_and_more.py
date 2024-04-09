# Generated by Django 5.0.3 on 2024-04-09 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TweetRecognitionApp', '0004_alter_topic_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='negativeWords',
            field=models.JSONField(default=['default', 'words']),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='neutralWords',
            field=models.JSONField(default=['default', 'words']),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='positiveWords',
            field=models.JSONField(default=['default', 'words']),
            preserve_default=False,
        ),
    ]
