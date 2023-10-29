# Create a command line tool that reads the name of a csv file and the kind of recommendation to create.
# The csv file will have the following format:
# id_proposal, candidacy_slug, order
# And load the data into the database.

import csv
import sys
import os
import django
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_expertos.settings')
django.setup()

from recommendations.models import Proposal, Candidacy, ProposalRecommendation, Recommendation

def read_recommendations(csv_file, kind):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proposal = Proposal.objects.get(id=row['id_proposal'])
            candidacy = Candidacy.objects.get(slug=row['candidacy_slug'])
            recommendation, created = Recommendation.objects.get_or_create(candidacy=candidacy, kind=kind)
            proposal_recommendation = ProposalRecommendation.objects.create(proposal=proposal, recommendation=recommendation, order=row['order'])

if __name__ == '__main__':
    read_recommendations(sys.argv[1], sys.argv[2])
