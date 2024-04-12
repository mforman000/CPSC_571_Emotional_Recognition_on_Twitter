from django.db import models

class Topic(models.Model):
    topic = models.CharField(max_length=100)
    solo_bert_percent = models.JSONField()
    svm_bert_percent = models.JSONField()
    svm_bow_percentage = models.JSONField()
    positiveWords = models.JSONField()
    negativeWords = models.JSONField()
    neutralWords = models.JSONField()
    solo_bert_predicted_data = models.JSONField()
    svm_bert_predicted_data = models.JSONField()
    svm_bow_predicted_data = models.JSONField()
    solo_bert_actual_data = models.JSONField()
    svm_bert_actual_data = models.JSONField()
    svm_bow_actual_data = models.JSONField()


    def __str__(self):
        return self.topic
