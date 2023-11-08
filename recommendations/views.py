from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from .ids_seleccionados import ids_candidaturas

from recommendations.forms import RecommendationEvaluationForm
from .models import Candidacy, ChoosenRecommendation, Recommendation
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RecommendationEvaluation
from .forms import ChoosenRecommendationForm, RecommendationEvaluationForm
from .models import Candidacy

# Create a class based view for listing Candidacy objects


class CandidacyListView(ListView):
    model = Candidacy
    template_name = 'candidacies.html'
    context_object_name = 'candidacies'
    paginate_by = 15

    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        return queryset.filter(slug__in=ids_candidaturas)

# Create a class based view for showing a Candidacy object
class CandidacyDetailView(DetailView):
    model = Candidacy
    template_name = 'candidacy.html'
    context_object_name = 'candidacy'

# Create a class based view for creating a ChoosenRecommendation using the ChoosenRecommendationForm
# it should receive the candidacy slug
# it should pass the candidacy to the template
# the template used should be candidacy.html
# the user should be logged in to access this view

class ChoosenRecommendationCreateView(LoginRequiredMixin, CreateView):
    model = Recommendation
    form_class = RecommendationEvaluationForm
    template_name = 'candidacy.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ChoosenRecommendationCreateView, self).get_context_data(**kwargs)
        context['candidacy'] = Candidacy.objects.get(slug=self.kwargs['slug'])
        return context

    def get_form_kwargs(self):
        kwargs = super(ChoosenRecommendationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['candidacy'] = Candidacy.objects.get(slug=self.kwargs['slug'])
        return kwargs


# Create a class based view for creating a ChoosenRecommendation using the ChoosenRecommendationForm
# it should receive the candidacy slug
# it should pass the candidacy to the template

class ChoosenRecommendationCreateView(LoginRequiredMixin, CreateView):
    model = ChoosenRecommendation
    form_class = ChoosenRecommendationForm
    template_name = 'candidacy.html'

    # if a previous ChoosenRecommendation object exists for the user and candidacy, raise 404
    def dispatch(self, request, *args, **kwargs):
        if ChoosenRecommendation.objects.filter(user=self.request.user, candidacy__slug=self.kwargs['slug']).exists():
            raise Http404
        return super(ChoosenRecommendationCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChoosenRecommendationCreateView, self).get_context_data(**kwargs)
        context['candidacy'] = Candidacy.objects.get(slug=self.kwargs['slug'])
        return context

    def get_form_kwargs(self):
        kwargs = super(ChoosenRecommendationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['candidacy'] = Candidacy.objects.get(slug=self.kwargs['slug'])
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(ChoosenRecommendationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('candidacies')




# Create a class based view for creating a RecommendationEvaluation object
# it should receive the recommendation slug and the user from the request
# it should redirect to the recommendation detail page
# the user should be logged in to access this view
# the user should be logged in to access this view

class RecommendationEvaluationCreateView(LoginRequiredMixin, CreateView):
    model = RecommendationEvaluation
    form_class = RecommendationEvaluationForm
    template_name = 'recommendation.html'

    # If a previous RecommendationEvaluation object exists for the user and recommendation, raise 404
    def dispatch(self, request, *args, **kwargs):
        if RecommendationEvaluation.objects.filter(user=self.request.user, recommendation=self.kwargs['pk']).exists():
            raise Http404
        return super(RecommendationEvaluationCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(RecommendationEvaluationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['recommendation'] = Recommendation.objects.get(id=self.kwargs['pk'])
        return kwargs
    
    # Pass recommendation to the template
    def get_context_data(self, **kwargs):
        context = super(RecommendationEvaluationCreateView, self).get_context_data(**kwargs)
        context['recommendation'] = Recommendation.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('candidacy', kwargs={'slug': self.kwargs['slug']})
    