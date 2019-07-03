from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['POST'])
def upload_file(request):
    #if request.method == 'POST':
        #handle_uploaded_file(request.FILES['file'])
    return JsonResponse({'text':"abc",'emotions':{'angry': 0.2, 'happy':0.3}})
