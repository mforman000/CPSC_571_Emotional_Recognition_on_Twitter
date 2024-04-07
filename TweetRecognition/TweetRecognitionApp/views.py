from django.shortcuts import render
from .models import Topic
from django.http import JsonResponse

# Create your views here.
def index(request):
    topics = Topic.objects.values_list('topic', flat=True).distinct()
    return render(request, 'index.html', {'topics' : topics})

def pie_chart_data(request):
    topic = request.GET.get('topic')
    data_objects = Topic.objects.filter(topic = topic)
    valuesList = [data.value for data in data_objects]
    data = {
        'labels' : ["positive", "Negative", "Neutral"],
        'data' : valuesList[0]
    }
    return(JsonResponse(data))
