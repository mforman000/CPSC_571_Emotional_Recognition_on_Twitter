# Generated by Django 5.0.3 on 2024-04-12 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TweetRecognitionApp', '0006_topic_actual_data_topic_predicted_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='actual_data',
            new_name='solo_bert_actual_data',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='predicted_data',
            new_name='solo_bert_percentages',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='value',
        ),
        migrations.AddField(
            model_name='topic',
            name='solo_bert_predicted_data',
            field=models.JSONField(default=[1, 2, 0]),
            preserve_default=False,
        ),
    ]
