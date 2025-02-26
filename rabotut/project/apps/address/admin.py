from django.contrib import admin
from django.contrib.gis import forms
from django.contrib.gis.db.models import PointField

from .forms import CityAdminForm
from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'id')
    formfield_overrides = {
        PointField: {
            'widget': forms.OSMWidget(
                attrs={
                    'default_lat': 54.177,
                    'default_lon': 45.1833,
                },
            ),
        },
    }
    form = CityAdminForm
