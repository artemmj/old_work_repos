from itertools import islice

from openpyxl import load_workbook

from apps import app
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.template.models import Template, TemplateExport


@app.task
def import_template_imp_celery_wrapper(file: str):
    """Обертка для асинхронного выполнения."""
    return ImportTemplateImpService(file=file).process()


@app.task
def import_template_exp_celery_wrapper(file: str):
    """Обертка для асинхронного выполнения."""
    return ImportTemplateExpService(file=file).process()


class ImportTemplateService(AbstractService):
    def __init__(self, file: str):
        self.file = File.objects.get(id=file).file.path
        self.wb = load_workbook(filename=self.file)
        self.sheet = self.wb.worksheets[0]
        self.template_data = {}
        self.errors = []

    def _prepare_data(self):
        try:
            for _, row in enumerate(islice(self.sheet.rows, 0, None)):  # noqa: WPS468
                name, value = row[:2]
                if name.value == 'fields':
                    self.template_data[name.value] = value.value.split(',')
                else:
                    self.template_data[name.value] = value.value
        except Exception as e:
            self.errors.append(str(e))


class ImportTemplateImpService(ImportTemplateService):
    def process(self):
        self._prepare_data()
        template = Template.objects.create(**self.template_data)
        return {'template_id': template.id, 'errors': self.errors}


class ImportTemplateExpService(ImportTemplateService):
    def process(self):
        self._prepare_data()
        template = TemplateExport.objects.create(**self.template_data)
        return {'template_id': template.id, 'errors': self.errors}
