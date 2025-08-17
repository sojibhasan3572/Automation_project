from automation_dj.celery import app
from django.core.management import call_command
from .utlis import send_email_notification
import time

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    # notify the user by email
    mail_subject = 'Import Data Completed'
    message = 'Your data import has been successful'
    to_email = 'sojibhasan5800@gmail.com'
    send_email_notification(mail_subject, message, [to_email])
    return 'Data imported successfully.'