from automation_dj.celery import app
from django.core.management import call_command
import time

@app.task
def import_data_task(file_path,model_name):
   try:
    call_command('importdata',file_path,model_name)

   except Exception as e:
    print(e)
         
    return 'task exitucted successfully'