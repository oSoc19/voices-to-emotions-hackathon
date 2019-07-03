from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .speechtoimage import create_spectrogram
import os

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        create_spectrogram(uploaded_file_url)

        os.remove(uploaded_file_url)

        newName = uploaded_file_url.split(".")[0] + ".png"

        result = "no AI yet" # send newName to AI

        os.remove(newName)

        return JsonResponse(result,safe=False)
    return JsonResponse("oops something wrong")