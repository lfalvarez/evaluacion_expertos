from django.contrib import admin

# Register the admin section for the Candidacy model
from .models import Candidacy
admin.site.register(Candidacy)

# Register the admin section for the proposal model
from .models import Proposal
admin.site.register(Proposal)

# Register the admin section for the ChoosenRecommendation model
from .models import ChoosenRecommendation
admin.site.register(ChoosenRecommendation)
