from apps import app
from apps.helpers.storages import save_file_to_db
from apps.stories.services import StoriesViewsReportService


@app.task
def generate_stories_views_report_task(start: str, end: str):
    """Селери таска для генерации отчета по просмотрам сторис."""
    workbook = StoriesViewsReportService(start, end).process()
    filename = f'stories_report_from_{start}_to_{end}.xlsx'
    workbook.save(filename)
    return save_file_to_db(filename)
