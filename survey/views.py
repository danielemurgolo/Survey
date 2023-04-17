from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.views import View
from django.db.models import Q
from .models import Survey, RadioQuestion, RadioAnswer, IntegerQuestion, CountryQuestion
from .models import Response, RadioResponse, IntegerResponse, CountryResponse
from cities_light.models import Country, Region

# Create your views here.


class SurveyListView(ListView):
    model = Survey
    template_name = "survey_list.html"


class SurveyDetailView(DetailView):
    model = Survey
    template_name = "survey_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = context["object"]
        context["radio_questions"] = survey.radioquestion_set.all()
        context["integer_questions"] = survey.integerquestion_set.all()
        context["country_question"] = survey.countryquestion_set.first()
        context["countries"] = Country.objects.all()
        context["regions"] = Region.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        response = Response.objects.create(survey=survey)

        for key, value in request.POST.items():
            if key.startswith("radio_question_"):
                question_id = int(key[len("radio_question_") :])
                question = RadioQuestion.objects.get(id=question_id)
                answer = RadioAnswer.objects.get(id=value)
                RadioResponse.objects.create(
                    response=response, question=question, answer=answer
                )
            elif key.startswith("integer_question_"):
                question_id = int(key[len("integer_question_") :])
                question = IntegerQuestion.objects.get(id=question_id)
                IntegerResponse.objects.create(
                    response=response, question=question, value=value
                )
            elif key == "country":
                question = survey.countryquestion_set.first()
                question_id = question.id
                CountryResponse.objects.create(
                    response=response,
                    question=question,
                    country=Country.objects.get(id=int(value)),
                    region=Region.objects.get(id=1),
                )
            elif key == "region":
                question = survey.countryquestion_set.first()
                question_id = question.id
                CountryResponse.objects.filter(
                    Q(response=response) & Q(question=question)
                ).update(region=Region.objects.get(id=int(value)))
        return redirect(reverse("survey:thank_you"))


class ThankYouView(View):
    def get(self, request):
        return render(request, "thank_you.html")


class EditSurveyView(UpdateView):
    model = Survey
    template_name = "survey_edit.html"
    fields = ["name", "description"]


class DeleteSurveyView(DeleteView):
    model = Survey
    template_name = "survey_delete.html"
    success_url = reverse_lazy("survey:home")


class CreateSurveyView(CreateView):
    model = Survey
    template_name = "survey_new.html"
    fields = ["name", "description"]
