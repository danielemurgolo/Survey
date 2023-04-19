from django.urls import path


from .views import (
    SurveyListView,
    SurveyDetailView,
    ThankYouView,
    EditSurveyView,
    DeleteSurveyView,
    CreateSurveyView,
    CreateRadioQuestionView,
    ajax_load_regions,
)

app_name = "survey"

urlpatterns = [
    path("new/", CreateSurveyView.as_view(), name="new"),
    path("<int:pk>/", SurveyDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", EditSurveyView.as_view(), name="edit"),
    path("<int:pk>/delete", DeleteSurveyView.as_view(), name="delete"),
    path("thank-you/", ThankYouView.as_view(), name="thank_you"),
    path("ajax/load-regions/", ajax_load_regions, name="ajax_load_regions"),
    path(
        "radio-question/", CreateRadioQuestionView.as_view(), name="new_radio_question"
    ),
    path("", SurveyListView.as_view(), name="home"),
]
