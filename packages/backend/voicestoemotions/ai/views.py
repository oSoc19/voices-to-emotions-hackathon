from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .speechtoimage import create_spectrogram
from .Predict import get_prediction
import os
import datetime

upload_dir = './uploaded'


@api_view(['POST'])
def upload_file(request):
    print(len(request.FILES))
    if request.method == 'POST' and request.FILES['myfile']:

        print(request.FILES['myfile'])

        file_name = datetime.datetime.now().isoformat() + '.wav'
        file_name = file_name.replace(":","-")
        save_path = os.path.join(upload_dir, file_name)

        myfile = request.FILES['myfile']

        print(myfile)

        fs = FileSystemStorage()
        filename = fs.save(save_path, myfile)
        uploaded_file_url = fs.url(filename)

        spectrogram_filename = create_spectrogram(uploaded_file_url)

        prediction, mapped_predictions = get_prediction(spectrogram_filename)

        result = {
            'text': "Dogs are sitting by the door",
            'emotion': prediction
        }

        return JsonResponse(result, safe=False)
    return JsonResponse("oops something wrong")
