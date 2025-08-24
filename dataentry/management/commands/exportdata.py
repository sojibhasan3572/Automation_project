from django.core.management.base import BaseCommand,CommandError
from django.apps import apps
from django.http import HttpResponse
from dataentry.utlis import generate_csv_file
import csv
import datetime


# Proposed command - python manage.py exportdata  model_name
class Command(BaseCommand):
    help = "Export data from the database to a CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help="Name of the Model")
    
    
    def handle(self,*args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        #Search Model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label,model_name)
                break # stop executing once the model is found
            except LookupError:
                continue

        if not model:
            raise CommandError(f'Model "{model_name}" is not found') 
        
        # fetch the data from the database
        data = model.objects.all()

        # generate csv file path
        file_path = generate_csv_file(model_name)
        
        with open(file_path , 'w', newline='') as file:
            writer = csv.writer(file)

            # write the CSV header
            writer.writerow([ field.name for field in model._meta.fields])

            for record in data:
                writer.writerow([ getattr(record, field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS('Data Exported from CSV successfully!'))


