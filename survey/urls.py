from django.urls import path


from .views import SurveyListView, SurveyDetailView, ThankYouView

app_name = "survey"

urlpatterns = [
    path("<int:pk>/", SurveyDetailView.as_view(), name="detail"),
    path("thank-you/", ThankYouView.as_view(), name="thank_you"),
    path("", SurveyListView.as_view(), name="home"),
]
