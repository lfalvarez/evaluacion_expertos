## Create a form for creating a new RecommendationEvaluation passing current user and recommendation as hidden fields

from django import forms

from recommendations.models import RecommendationEvaluation, ChoosenRecommendation

class RecommendationEvaluationForm(forms.ModelForm):
    class Meta:
        model = RecommendationEvaluation
        fields = ['likert']
        widgets = {
            'likert': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.recommendation = kwargs.pop('recommendation')
        super(RecommendationEvaluationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(RecommendationEvaluationForm, self).save(commit=False)
        instance.user = self.user
        instance.recommendation = self.recommendation
        if commit:
            instance.save()
        return instance
    
# Create a form for creating a new ChoosenRecommendation passing candidacy and user as hidden fields
# it should only list recommendations that are in the candidacy
# only one recommendation should be choosen

class ChoosenRecommendationForm(forms.ModelForm):
    class Meta:
        model = ChoosenRecommendation
        fields = ['recommendation']
        widgets = {
            'recommendation': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.candidacy = kwargs.pop('candidacy')
        super(ChoosenRecommendationForm, self).__init__(*args, **kwargs)
        # recomendations should only be the ones in the candidacy and they should be ordered randomly
        self.fields['recommendation'].queryset = self.candidacy.recommendations.all().order_by('?')
        self.fields['recommendation'].required = False

    def save(self, commit=True):
        instance = super(ChoosenRecommendationForm, self).save(commit=False)
        instance.user = self.user
        instance.candidacy = self.candidacy
        print(instance)
        if commit:
            instance.save()
        return instance
