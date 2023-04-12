from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from .models import Survey, RadioQuestion, RadioAnswer, IntegerQuestion, CountryQuestion
from .models import Response, RadioResponse, IntegerResponse, CountryResponse

# Create your views here.


class SurveyDetailView(DetailView):
    model = Survey
    template_name = "survey_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = context["object"]
        context["radio_question"] = survey.radioquestion_set.all()
        context["integer_question"] = survey.integerquestion_set.all()
        context["country_question"] = survey.countryquestion_set.all()

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
                question = CountryQuestion.objects.get(id=int(value))
                CountryResponse.objects.create(
                    response=response, question=question, country_id=value
                )
        return redirect(reverse("survey:thank_you"))
