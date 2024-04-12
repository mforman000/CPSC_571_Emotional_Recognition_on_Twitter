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

    solo_bert_actual_data_list = data_objects.values_list('solo_bert_actual_data', flat=True)
    solo_bert_predicted_data_list = data_objects.values_list('solo_bert_predicted_data', flat=True)

    solo_bert_confusion_matrix_data = generate_confusion_matrix(solo_bert_actual_data_list[0], solo_bert_predicted_data_list[0]).tolist()

    svm_bert_actual_data_list = data_objects.values_list('svm_bert_actual_data', flat=True)
    svm_bert_predicted_data_list = data_objects.values_list('svm_bert_predicted_data', flat=True)

    svm_bert_confusion_matrix_data = generate_confusion_matrix(svm_bert_actual_data_list[0], svm_bert_predicted_data_list[0]).tolist()

    svm_bow_actual_data_list = data_objects.values_list('svm_bow_actual_data', flat=True)
    svm_bow_predicted_data_list = data_objects.values_list('svm_bow_predicted_data', flat=True)

    svm_bow_confusion_matrix_data = generate_confusion_matrix(svm_bow_actual_data_list[0], svm_bow_predicted_data_list[0]).tolist()

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


    initial_data['solo_bert_confusion_matrix'] = solo_bert_confusion_matrix_data
    initial_data['solo_bert_accuracy_0'] = str(round(solo_bert_confusion_matrix_data[0][0]/(solo_bert_confusion_matrix_data[0][0] + solo_bert_confusion_matrix_data[1][0] + solo_bert_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    initial_data['solo_bert_accuracy_1'] = str(round(solo_bert_confusion_matrix_data[1][1]/(solo_bert_confusion_matrix_data[0][1] + solo_bert_confusion_matrix_data[1][1] + solo_bert_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    initial_data['solo_bert_accuracy_2'] = str(round(solo_bert_confusion_matrix_data[2][2]/(solo_bert_confusion_matrix_data[0][2] + solo_bert_confusion_matrix_data[1][2] + solo_bert_confusion_matrix_data[2][2]) * 100, 1)) + "%"

    initial_data['svm_bert_confusion_matrix'] = svm_bert_confusion_matrix_data
    initial_data['svm_bert_accuracy_0'] = str(round(svm_bert_confusion_matrix_data[0][0]/(svm_bert_confusion_matrix_data[0][0] + svm_bert_confusion_matrix_data[1][0] + svm_bert_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    initial_data['svm_bert_accuracy_1'] = str(round(svm_bert_confusion_matrix_data[1][1]/(svm_bert_confusion_matrix_data[0][1] + svm_bert_confusion_matrix_data[1][1] + svm_bert_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    initial_data['svm_bert_accuracy_2'] = str(round(svm_bert_confusion_matrix_data[2][2]/(svm_bert_confusion_matrix_data[0][2] + svm_bert_confusion_matrix_data[1][2] + svm_bert_confusion_matrix_data[2][2]) * 100, 1)) + "%"

    initial_data['svm_bow_confusion_matrix'] = svm_bow_confusion_matrix_data
    initial_data['svm_bow_accuracy_0'] = str(round(svm_bow_confusion_matrix_data[0][0]/(svm_bow_confusion_matrix_data[0][0] + svm_bow_confusion_matrix_data[1][0] + svm_bow_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    initial_data['svm_bow_accuracy_1'] = str(round(svm_bow_confusion_matrix_data[1][1]/(svm_bow_confusion_matrix_data[0][1] + svm_bow_confusion_matrix_data[1][1] + svm_bow_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    initial_data['svm_bow_accuracy_2'] = str(round(svm_bow_confusion_matrix_data[2][2]/(svm_bow_confusion_matrix_data[0][2] + svm_bow_confusion_matrix_data[1][2] + svm_bow_confusion_matrix_data[2][2]) * 100, 1)) + "%"


    return render(request, 'index.html', initial_data)

def pie_chart_data(request):
    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = topic)
    solo_bert_percentages = [data.solo_bert_percent for data in data_objects]
    svm_bert_percentages = [data.svm_bert_percent for data in data_objects]
    svm_bow_percentages = [data.svm_bow_percentage for data in data_objects]
    data = {
        'labels' : ["Negative", "Neutral", "Positive"],
        'solo_bert_data' : solo_bert_percentages[0],
        'svm_bert_data' : svm_bert_percentages[0],
        'svm_bow_data' : svm_bow_percentages[0]
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

    solo_bert_actual_data_list = data_objects.values_list('solo_bert_actual_data', flat=True)
    solo_bert_predicted_data_list = data_objects.values_list('solo_bert_predicted_data', flat=True)

    solo_bert_confusion_matrix_data = generate_confusion_matrix(solo_bert_actual_data_list[0], solo_bert_predicted_data_list[0]).tolist()
    cm_data['solo_bert_confusion_matrix_data'] = solo_bert_confusion_matrix_data
    cm_data['solo_bert_accuracy_0'] = str(round(solo_bert_confusion_matrix_data[0][0]/(solo_bert_confusion_matrix_data[0][0] + solo_bert_confusion_matrix_data[1][0] + solo_bert_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    cm_data['solo_bert_accuracy_1'] = str(round(solo_bert_confusion_matrix_data[1][1]/(solo_bert_confusion_matrix_data[0][1] + solo_bert_confusion_matrix_data[1][1] + solo_bert_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    cm_data['solo_bert_accuracy_2'] = str(round(solo_bert_confusion_matrix_data[2][2]/(solo_bert_confusion_matrix_data[0][2] + solo_bert_confusion_matrix_data[1][2] + solo_bert_confusion_matrix_data[2][2]) * 100, 1)) + "%"
    
    svm_bert_actual_data_list = data_objects.values_list('svm_bert_actual_data', flat=True)
    svm_bert_predicted_data_list = data_objects.values_list('svm_bert_predicted_data', flat=True)
    svm_bert_confusion_matrix_data = generate_confusion_matrix(svm_bert_actual_data_list[0], svm_bert_predicted_data_list[0]).tolist()
    cm_data['svm_bert_confusion_matrix_data'] = svm_bert_confusion_matrix_data
    cm_data['svm_bert_accuracy_0'] = str(round(svm_bert_confusion_matrix_data[0][0]/(svm_bert_confusion_matrix_data[0][0] + svm_bert_confusion_matrix_data[1][0] + svm_bert_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    cm_data['svm_bert_accuracy_1'] = str(round(svm_bert_confusion_matrix_data[1][1]/(svm_bert_confusion_matrix_data[0][1] + svm_bert_confusion_matrix_data[1][1] + svm_bert_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    cm_data['svm_bert_accuracy_2'] = str(round(svm_bert_confusion_matrix_data[2][2]/(svm_bert_confusion_matrix_data[0][2] + svm_bert_confusion_matrix_data[1][2] + svm_bert_confusion_matrix_data[2][2]) * 100, 1)) + "%"

    svm_bow_actual_data_list = data_objects.values_list('svm_bert_actual_data', flat=True)
    svm_bow_predicted_data_list = data_objects.values_list('svm_bert_predicted_data', flat=True)
    svm_bow_confusion_matrix_data = generate_confusion_matrix(svm_bow_actual_data_list[0], svm_bow_predicted_data_list[0]).tolist()
    cm_data['svm_bow_confusion_matrix_data'] = svm_bow_confusion_matrix_data
    cm_data['svm_bow_accuracy_0'] = str(round(svm_bow_confusion_matrix_data[0][0]/(svm_bow_confusion_matrix_data[0][0] + svm_bow_confusion_matrix_data[1][0] + svm_bow_confusion_matrix_data[2][0]) * 100, 1)) + "%"
    cm_data['svm_bow_accuracy_1'] = str(round(svm_bow_confusion_matrix_data[1][1]/(svm_bow_confusion_matrix_data[0][1] + svm_bow_confusion_matrix_data[1][1] + svm_bow_confusion_matrix_data[2][1]) * 100, 1)) + "%"
    cm_data['svm_bow_accuracy_2'] = str(round(svm_bow_confusion_matrix_data[2][2]/(svm_bow_confusion_matrix_data[0][2] + svm_bow_confusion_matrix_data[1][2] + svm_bow_confusion_matrix_data[2][2]) * 100, 1)) + "%"
    return(JsonResponse(cm_data, safe=False))

def generate_confusion_matrix(y_actual, y_pred):

    c_matrix = confusion_matrix(y_actual, y_pred)
    return c_matrix
