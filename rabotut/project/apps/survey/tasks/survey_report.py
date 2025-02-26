from apps import app
from apps.helpers.storages import save_file_to_db
from apps.survey.services import SurveyReportService


@app.task
def generate_survey_report(survey_id: str):
    """Задача, которая запускает сервис генерации отчета."""
    workbook = SurveyReportService().process(survey_id)
    filename = f'survey_report_{survey_id}.xlsx'
    workbook.save(filename)
    return save_file_to_db(filename)
