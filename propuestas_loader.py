import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_expertos.settings')
from django.conf import settings
from evaluacion_expertos.settings import DEBUG, INSTALLED_APPS, DATABASES
import django

settings.configure(DEBUG=DEBUG, INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES)
django.setup()

# Create a process for laoding proposals from csv file named propuestas.csv with fields: id, title, description, classification
with open('propuestas.csv') as csvfile:
    from recommendations.models import Proposal
    reader = csv.DictReader(csvfile, fieldnames=['id', 'title', 'description', 'classification'])
    # jump header lines
    next(reader)
    for row in reader:
        proposal = Proposal.objects.get_or_create(id=int(row['id']), title=row['title'], description=row['description'], classification=row['classification'])
