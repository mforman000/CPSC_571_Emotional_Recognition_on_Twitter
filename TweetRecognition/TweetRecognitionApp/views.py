import matplotlib
matplotlib.use('agg')

from django.shortcuts import render
from .models import Topic
from django.http import JsonResponse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.metrics import confusion_matrix
import numpy as np
import base64


# Create your views here.
def index(request):
    initial_data = {}

    topics = Topic.objects.values_list('topic', flat=True).distinct()
    initial_data['topics'] = topics

    

    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = 'Airlines')

    actual_data_list = data_objects.values_list('actual_data', flat=True)
    predicted_data_list = data_objects.values_list('predicted_data', flat=True)

    confusion_matrix_data = generate_confusion_matrix(actual_data_list[0], predicted_data_list[0]).tolist()

    positiveWordList = data_objects.values_list('positiveWords', flat=True)
    if (not positiveWordList):
        positiveWordList = ["no", "words", "present", "positive"]
    else:
        positiveWordList = positiveWordList[0]

    negativeWordList = data_objects.values_list('negativeWords', flat=True)
    if (not negativeWordList):
        negativeWordList = ["no", "words", "present", "negative"]
    else:
        negativeWordList = negativeWordList[0]

    neutralWordList = data_objects.values_list('neutralWords', flat=True)
    if (not neutralWordList):
        neutralWordList = ["no", "words", "present", "neutral"]
    else:
        neutralWordList = neutralWordList[0]
    # wordList = ["this", "is", "the", "word", "list"]
    positive_word_freq = {word: positiveWordList.count(word) for word in set(positiveWordList)}
    negative_word_freq = {word: negativeWordList.count(word) for word in set(negativeWordList)}
    neutral_word_freq = {word: neutralWordList.count(word) for word in set(neutralWordList)}
    initial_data['positiveWordcloud'] = generate_wordcloud(positive_word_freq)
    initial_data['negativeWordcloud'] = generate_wordcloud(negative_word_freq)
    initial_data['neutralWordcloud'] = generate_wordcloud(neutral_word_freq)
    initial_data['confusion_matrix'] = confusion_matrix_data
    initial_data['accuracy_0'] = str(round(confusion_matrix_data[0][0]/(confusion_matrix_data[0][0] + confusion_matrix_data[1][0] + confusion_matrix_data[2][0]) * 100, 1)) + "%"
    initial_data['accuracy_1'] = str(round(confusion_matrix_data[1][1]/(confusion_matrix_data[0][1] + confusion_matrix_data[1][1] + confusion_matrix_data[2][1]) * 100, 1)) + "%"
    initial_data['accuracy_2'] = str(round(confusion_matrix_data[2][2]/(confusion_matrix_data[0][2] + confusion_matrix_data[1][2] + confusion_matrix_data[2][2]) * 100, 1)) + "%"

    return render(request, 'index.html', initial_data)

def pie_chart_data(request):
    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = topic)
    valuesList = [data.value for data in data_objects]
    data = {
        'labels' : ["positive", "Negative", "Neutral"],
        'data' : valuesList[0]
    }
    return(JsonResponse(data))

def generate_wordcloud(word_freq):
    wordCloud = WordCloud(width = 800, height = 400,).generate_from_frequencies(word_freq)

    plt.figure(figsize=(8,4))
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    img_str =  "data:image/png;base64," + base64.b64encode(image_png).decode()
    return img_str

def regenerate_wordcloud(request):
    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = topic)

    positiveWordList = data_objects.values_list('positiveWords', flat=True)
    if (not positiveWordList):
        positiveWordList = ["no", "words", "present", "positive"]
    else:
        positiveWordList = positiveWordList[0]

    negativeWordList = data_objects.values_list('negativeWords', flat=True)
    if (not negativeWordList):
        negativeWordList = ["no", "words", "present", "negative"]
    else:
        negativeWordList = negativeWordList[0]

    neutralWordList = data_objects.values_list('neutralWords', flat=True)
    if (not neutralWordList):
        neutralWordList = ["no", "words", "present", "neutral"]
    else:
        neutralWordList = neutralWordList[0]
    positive_word_freq = {word: positiveWordList.count(word) for word in set(positiveWordList)}
    negative_word_freq = {word: negativeWordList.count(word) for word in set(negativeWordList)}
    neutral_word_freq = {word: neutralWordList.count(word) for word in set(neutralWordList)}
    word_cloud_data = {'positiveWordcloud': generate_wordcloud(positive_word_freq),
                         'negativeWordcloud': generate_wordcloud(negative_word_freq),
                         'neutralWordcloud': generate_wordcloud(neutral_word_freq)}
    return(JsonResponse(word_cloud_data))

def regenerate_confusion_matrix(request):
    cm_data = {}
    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = topic)

    actual_data_list = data_objects.values_list('actual_data', flat=True)
    predicted_data_list = data_objects.values_list('predicted_data', flat=True)

    confusion_matrix_data = generate_confusion_matrix(actual_data_list[0], predicted_data_list[0]).tolist()
    cm_data['confusion_matrix_data'] = confusion_matrix_data
    cm_data['accuracy_0'] = str(round(confusion_matrix_data[0][0]/(confusion_matrix_data[0][0] + confusion_matrix_data[1][0] + confusion_matrix_data[2][0]) * 100, 1)) + "%"
    cm_data['accuracy_1'] = str(round(confusion_matrix_data[1][1]/(confusion_matrix_data[0][1] + confusion_matrix_data[1][1] + confusion_matrix_data[2][1]) * 100, 1)) + "%"
    cm_data['accuracy_2'] = str(round(confusion_matrix_data[2][2]/(confusion_matrix_data[0][2] + confusion_matrix_data[1][2] + confusion_matrix_data[2][2]) * 100, 1)) + "%"
    return(JsonResponse(cm_data, safe=False))

def generate_confusion_matrix(y_actual, y_pred):

    c_matrix = confusion_matrix(y_actual, y_pred)
    return c_matrix
