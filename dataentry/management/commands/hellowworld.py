from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help ="print the hellow world"

    def handle(self, *args, **kwargs):
        self.stdout.write("hello world")