from django.contrib.gis import forms
from django.contrib.gis.geos import Point

from apps.helpers.consts import SRID

from .models import City


class CityAdminForm(forms.ModelForm):
    latitude = forms.FloatField(label='Широта', min_value=-90, max_value=90, required=False)  # noqa: WPS432
    longitude = forms.FloatField(label='Долгота', min_value=-180, max_value=180, required=False)  # noqa: WPS432

    class Meta:
        model = City
        exclude: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('location', None)
        if isinstance(coordinates, Point):
            longitude, latitude = coordinates.tuple
            self.initial['longitude'] = longitude
            self.initial['latitude'] = latitude

    def clean(self):
        """Метод валидации формы, переопределена логика сохранения 'местоположения'.

        - при добавлении в поле 'местоположение' записываются координаты, соответствующие выбранной на карте точке,
          если не указаны поля 'широта' и 'долгота', в противном случае - указанные в этих полях координаты
        - при изменении в поле 'местоположение' записываются те параметры, которые изменялись,
          если ни один из этих параметров не None, при одновременном изменении - данные полей 'широта' и 'долгота'.
        """
        form_data = super().clean()
        latitude = form_data.get('latitude')
        longitude = form_data.get('longitude')
        if latitude and longitude:
            if latitude != self.initial.get('latitude') or longitude != self.initial.get('longitude'):
                form_data['location'] = Point((longitude, latitude), srid=SRID)
        return form_data
