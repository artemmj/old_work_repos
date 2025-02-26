from django_filters import CharFilter, FilterSet


class CarFilterSet(FilterSet):
    brand = CharFilter(field_name='car_brand__title_brand')
    model = CharFilter(field_name='car_model__title_model')
    body_type = CharFilter(field_name='body_type__title_body_type')
    generation = CharFilter(field_name='generation__title_generation')
    gearbox = CharFilter(field_name='gearbox_type__title_gearbox_type')
    drive_type = CharFilter(field_name='drive_type__title_drive_type')
