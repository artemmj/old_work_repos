from django.contrib import admin

from apps.inspection.models.client import Client
from apps.inspection.models.completeness import Completeness
from apps.inspection.models.damage import Damage
from apps.inspection.models.documents import Documents
from apps.inspection.models.equipment import Equipment
from apps.inspection.models.inspection import Inspection
from apps.inspection.models.inspection_note import InspectionNote
from apps.inspection.models.lift import Lift
from apps.inspection.models.paintwork import Paintwork
from apps.inspection.models.photos import Photos
from apps.inspection.models.sign_client import SignClient
from apps.inspection.models.sign_inspector import SignInspector
from apps.inspection.models.technical import Technical
from apps.inspection.models.tires import Tires
from apps.inspection.models.video import Video
from apps.inspection_task.models.task import InspectionTaskCar


class InspectionTaskCarInline(admin.StackedInline):
    model = InspectionTaskCar
    extra = 0
    raw_id_fields = ('brand', 'model')


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspector', 'address', 'status')
    readonly_fields = ('complete_date', 'status')
    inlines = (InspectionTaskCarInline,)


@admin.register(InspectionNote)
class InspectionNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'inspection')
    raw_id_fields = ('inspection',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Completeness)
class CompletenessAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Documents)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Tires)
class TiresAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Paintwork)
class PaintworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Technical)
class TechnicalStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Lift)
class LiftInspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Damage)
class DamageCheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspection', 'created_at')


@admin.register(SignClient)
class SignClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


@admin.register(SignInspector)
class SignInspectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
