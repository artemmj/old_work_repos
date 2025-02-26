from django.utils import timezone
from django_lifecycle import hook


class InspectionUpdateDateMixin:

    @hook('after_create')
    def update_date(self):
        if self.inspection:
            self.inspection.updated_at = timezone.now()
            self.inspection.save()

        if self.accreditation_inspection:
            self.accreditation_inspection.updated_at = timezone.now()
            self.accreditation_inspection.save()

    @hook('after_update')
    def update_inspection_date(self):
        if self.inspection:
            self.inspection.updated_at = timezone.now()
            self.inspection.save()

        if self.accreditation_inspection:
            self.accreditation_inspection.updated_at = timezone.now()
            self.accreditation_inspection.save()
