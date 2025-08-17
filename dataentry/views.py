from django.shortcuts import render,redirect
from .utlis import get_all_custom_models,check_csv_errors
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from .tasks import import_data_task
# Create your views here.
def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # store this file inside the Upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # construct the full path
        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        file_path = base_url+relative_path

        # check for the csv errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')
        return redirect('import_data')

    else:
        custom_models = get_all_custom_models()
        context={
            'custom_models':custom_models
        }
        return render(request,'dataentry/importdata.html',context)
