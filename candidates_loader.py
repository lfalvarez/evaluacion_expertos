import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_expertos.settings')
from django.conf import settings
from evaluacion_expertos.settings import DEBUG, INSTALLED_APPS, DATABASES
import django

settings.configure(DEBUG=DEBUG, INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES)
django.setup()

with open('candidatos_comprometidos_con_partido_y_pacto.csv') as csvfile:
    from recommendations.models import Candidacy, Pact, Party, Position
    # fieldnames are position,pact,party,cantidad_compromisos,name,slug
    reader = csv.DictReader(csvfile, fieldnames=['position', 'pact', 'party', 'cantidad_compromisos', 'name', 'slug'])
    # jump header
    next(reader)
    for row in reader:
        pact, created_pact = Pact.objects.get_or_create(name=row['pact'])
        party, created_party = Party.objects.get_or_create(name=row['party'])
        position, created_position = Position.objects.get_or_create(name=row['position'])
        candidacy = Candidacy.objects.get_or_create( name=row['name'], slug=row['slug'], party=party, position=position, pact=pact)