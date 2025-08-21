from automation_dj.celery import app
from dataentry.utlis import send_email_notification


@app.task
def send_email_task(mail_subject, message, to_email, attachment, email_id):
    print("i am task")
    send_email_notification(mail_subject, message, to_email, attachment, email_id)
    return 'Email sending task executed successfully.'