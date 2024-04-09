import matplotlib
matplotlib.use('agg')

from django.shortcuts import render
from .models import Topic
from django.http import JsonResponse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# Create your views here.
def index(request):
    initial_data = {}

    topics = Topic.objects.values_list('topic', flat=True).distinct()
    initial_data['topics'] = topics

    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = 'Airlines')

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



# def wordcloud_view(request):
#     topic = request.GET.get('topic')
#     data_objects = Topic.objects.filter(topic = topic)
#     # wordList = [data.positiveWords for data in data_objects]
#     wordList = ["this", "is", "the", "word", "list"]
#     word_freq = {word: wordList.count(word) for word in set(wordList)}
    
#     wordCloud = WordCloud(width = 800, height = 400,).generate_from_frequencies(word_freq)

#     plt.figure(figsize=(8,4))
#     plt.imshow(wordCloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.tight_layout()

#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getValue()
#     buffer.close()
#     img_str = "data:image/png;base64," + base64.b64encode(image_png).decode()

#     return render(request, 'index.html', {'wordcloud': img_str})
