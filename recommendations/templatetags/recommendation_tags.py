from django import template

from recommendations.models import ChoosenRecommendation

# Register a tag for returning true or false depending on the existence of a ChoosenRecommendation object for the user and candidacy
register = template.Library()

@register.simple_tag
def has_choosen_recommendation(user, candidacy):
    if ChoosenRecommendation.objects.filter(user=user, candidacy=candidacy).exists():
        return True
    return False
