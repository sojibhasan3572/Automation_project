from automation_dj.celery import app
from django.core.management import call_command
from .utlis import send_email_notification,generate_csv_file

import time

@app.task
def import_data_task(file_path, model_name,user_email):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    # notify the user by email
    mail_subject = 'Import Data Completed'
    message = 'Your data import has been successful'
    to_email = user_email
    send_email_notification(mail_subject, message, [to_email])
    return 'Data imported successfully.'


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    
    file_path = generate_csv_file(model_name)
    
    # Send email with the attachment
    mail_subject = 'Export Data Successful'
    message = 'Export data successful. Please find the attachment'
    to_email = "sojibhasan5800@gmail.com" # !!!!!!! Reques User Mail Send
    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return 'Export Data task executed successfully.'