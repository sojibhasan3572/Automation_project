from django.core.management.base import BaseCommand,CommandError
from django.apps import apps
from django.db.utils import DataError
import csv

# Proposed command - python manage.py importdata file_path model_name
class Command(BaseCommand):
    help = "Import data from CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="path to the CSV file")
        parser.add_argument('model_name', type=str, help="Name of the Model")
    
    
    def handle(self,*args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        #Search Model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label,model_name)
                break
            except LookupError:
                continue
        if not model:
            raise CommandError(f'Model "{model_name}" is not found') 
        
         # Get model fields without 'id'
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            # Get CSV headers without 'id'
            csv_header = [col for col in reader.fieldnames if col != 'id']

            if csv_header != model_fields:
                raise DataError (f"CSV file doesn't match with the {model_name} table fields")

            for row in reader:
                row.pop('id', None)
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))

