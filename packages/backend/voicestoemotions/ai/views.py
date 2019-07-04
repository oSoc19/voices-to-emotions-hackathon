from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .speechtoimage import create_spectrogram
import os
import datetime

upload_dir = './uploaded'


@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        file_name = datetime.datetime.now().isoformat() + '.wav'
        save_path = os.path.join(upload_dir, file_name)

        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(save_path, myfile)
        uploaded_file_url = fs.url(filename)

        spectrogram_filename = create_spectrogram(uploaded_file_url)

        # TODO: Predict based on this filename

        result = {
            'text': "text",
            'emotions': "sad"
        }

        return JsonResponse(result, safe=False)
    return JsonResponse("oops something wrong")
