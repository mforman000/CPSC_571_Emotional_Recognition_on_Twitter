# Generated by Django 5.0.3 on 2024-04-12 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TweetRecognitionApp', '0007_rename_actual_data_topic_solo_bert_actual_data_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='solo_bert_percentages',
            new_name='solo_bert_percent',
        ),
    ]
