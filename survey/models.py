from django.db import models
from cities_light.models import Country, Region

# from cities_light.models import Region, Country

# Create your models here.


class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class RadioQuestion(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question


class RadioAnswer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(RadioQuestion, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.answer


class IntegerQuestion(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question


# class Country(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return self.name


# class Region(models.Model):
#     name = models.CharField(max_length=200)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.name


class CountryQuestion(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question


class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class RadioResponse(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(RadioQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(RadioAnswer, on_delete=models.CASCADE)


class IntegerResponse(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(IntegerQuestion, on_delete=models.CASCADE)
    value = models.IntegerField()


class CountryResponse(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(CountryQuestion, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
