from django.db import models

#Createa a model for Party with name
class Party(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Create a model for Position with name
class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Create a model for Pact with name
class Pact(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create a model for Candidacy with name, slug
class Candidacy(models.Model): 
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    pact = models.ForeignKey(Pact, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

# Create a model for Proposal with title and description
class Proposal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    classification = models.CharField(max_length=255, default=None, null=True)

    def __str__(self):
        return self.title

# Create a model for Recommendation with candidacy, proposal_recommendation and kind wich is a choice field with values: 'random', 'knn', 'semantic'
class Recommendation(models.Model):
    candidacy = models.ForeignKey(Candidacy, on_delete=models.CASCADE, related_name='recommendations')
    kind = models.CharField(max_length=255, choices=[('random', 'random'), ('knn', 'knn'), ('semantic', 'semantic')])

    def __str__(self):
        return self.candidacy.name + ' - ' + self.kind

# Create a model for ProposalRecommendation with proposal and order
class ProposalRecommendation(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='proposal_recommendations')
    order = models.IntegerField()

    def __str__(self):
        return self.proposal.title

# Create a class for RecommendationEvaluation with recommendation, user and likert wich is a choice field with values: 'strongly_disagree', 'disagree', 'neutral', 'agree', 'strongly_agree'
class RecommendationEvaluation(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    # User is a foreign key to the User model that comes with Django
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    likert = models.CharField(max_length=255, choices=[('strongly_disagree', 'strongly_disagree'), ('disagree', 'disagree'), ('neutral', 'neutral'), ('agree', 'agree'), ('strongly_agree', 'strongly_agree')])

    def __str__(self):
        return self.recommendation.candidacy.name + ' - ' + self.recommendation.kind + ' - ' + str(self.user) + ' - ' + self.likert
    

# Create a class for ChoosenRecommendation with fields recommendation, user and candidacy
class ChoosenRecommendation(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    candidacy = models.ForeignKey(Candidacy, on_delete=models.CASCADE)

    def __str__(self):
        result = self.candidacy.name + ' - ' + str(self.user)
        if self.recommendation:
            result += ' - ' + self.recommendation.kind
        return result


