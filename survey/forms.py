from __future__ import unicode_literals
from django import forms
from cities_light.models import Country, Region


class CountryForm(forms.ModelForm):
    """
    Country model form.
    """

    class Meta:
        model = Country
        exclude = ("name_ascii", "slug", "geoname_id")


class RegionForm(forms.ModelForm):
    """
    Region model form.
    """

    class Meta:
        model = Region
        exclude = ("name_ascii", "slug", "geoname_id", "display_name", "geoname_code")
