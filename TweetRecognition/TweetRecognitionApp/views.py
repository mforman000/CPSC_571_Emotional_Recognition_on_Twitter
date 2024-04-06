from django.shortcuts import render
from .models import Topic
from django.http import JsonResponse

# Create your views here.
def index(request):
    topics = Topic.objects.all()
    return render(request, 'index.html', {'topics' : topics})

def pie_chart_data(request):
    data = {
        'labels' : ["positive", "Negative", "Neutral"],
        'data' : [10,20,30]
    }
    return(JsonResponse(data))
