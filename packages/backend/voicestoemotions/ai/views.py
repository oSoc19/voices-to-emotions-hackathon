from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .speechtoimage import graph_spectrogram

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        graph_spectrogram(uploaded_file_url)

        return JsonResponse(uploaded_file_url,safe=False)
    return JsonResponse("oops something wrong")