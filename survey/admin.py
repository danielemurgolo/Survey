from django.contrib import admin
from .models import Survey, RadioQuestion, RadioAnswer, CountryQuestion, IntegerQuestion

# Register your models here.

admin.site.register(Survey)
admin.site.register(RadioQuestion)
admin.site.register(RadioAnswer)
admin.site.register(IntegerQuestion)
