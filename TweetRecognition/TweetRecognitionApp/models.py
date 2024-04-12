from django.db import models

class Topic(models.Model):
    topic = models.CharField(max_length=100)
    value = models.JSONField()
    positiveWords = models.JSONField()
    negativeWords = models.JSONField()
    neutralWords = models.JSONField()
    predicted_data = models.JSONField()
    actual_data = models.JSONField()


    def __str__(self):
        return self.topic
