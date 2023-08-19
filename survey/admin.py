from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import Survey, RadioQuestion, RadioAnswer, CountryQuestion, IntegerQuestion


# Inline class for RadioAnswer
class RadioAnswerInline(NestedStackedInline):
    model = RadioAnswer
    extra = 1


# Inline class for RadioQuestion with RadioAnswerInline included
class RadioQuestionInline(NestedStackedInline):
    model = RadioQuestion
    extra = 1
    inlines = [RadioAnswerInline]  # Include RadioAnswerInline here


# Inline classes for other question types
class CountryQuestionInline(NestedStackedInline):
    model = CountryQuestion
    extra = 1


class IntegerQuestionInline(NestedStackedInline):
    model = IntegerQuestion
    extra = 1


class SurveyAdmin(NestedModelAdmin):
    inlines = [
        RadioQuestionInline,
        IntegerQuestionInline,
        CountryQuestionInline,
    ]


# Register models
admin.site.register(Survey, SurveyAdmin)
admin.site.register(RadioQuestion)
admin.site.register(RadioAnswer)
admin.site.register(IntegerQuestion)
admin.site.register(CountryQuestion)
