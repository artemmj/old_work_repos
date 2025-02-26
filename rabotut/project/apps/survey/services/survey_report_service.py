from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.helpers.services import AbstractService
from apps.survey.models import Answer


class SurveyReportService(AbstractService):
    """Сервис генерации отчета."""

    def process(self, survey_id: str) -> Workbook:
        wb = Workbook(write_only=True)
        ws = self._create_worksheet(wb)
        self._write_headers(ws)
        self._write_data(ws, survey_id)
        return wb

    def _create_worksheet(self, workbook: Workbook):
        """Создает рабочий лист и настраивает ширину колонок."""
        ws = workbook.create_sheet()
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 30
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 20
        ws.column_dimensions['G'].width = 30
        ws.column_dimensions['H'].width = 250
        return ws

    def _write_headers(self, worksheet: Worksheet):
        """Записывает заголовки в первую строку отчета."""
        headers = [
            'Департамент', 'Регион', 'ФИО', 'Бейдж', 'Номер телефона', 'Дата прохождения', 'Ответ', 'Открытый ответ',
        ]
        cells = [self._create_bold_cell(worksheet, header) for header in headers]
        worksheet.append(cells)

    def _create_bold_cell(self, worksheet, header):
        """Создает жирную ячейку с заданным значением."""
        cell = WriteOnlyCell(worksheet, value=header)
        cell.font = Font(bold=True)
        return cell

    def _write_data(self, worksheet: Worksheet, survey_id: str):
        """Записывает данные ответов в отчет."""
        answers = Answer.objects.filter(question__survey_id=survey_id)
        for answer in answers:
            option_names = [option.name for option in answer.options.all()]
            for option_name in option_names:
                row = self._create_data_row(answer, option_name)
                worksheet.append(row)

    def _create_data_row(self, answer: Answer, option_name: str):
        """Создает строку данных для ответа."""
        return [
            answer.user.department.name if answer.user.department else '-',
            ', '.join(answer.user.regions.values_list('name', flat=True)) if answer.user.regions.exists() else '-',
            f'{answer.user.last_name} {answer.user.first_name} {answer.user.middle_name}',
            '-',  # Позиция для бейджа
            str(answer.user.phone),
            answer.created_at.strftime('%Y.%m.%d, %H:%M:%S'),
            option_name,
            answer.self_option_answer if answer.self_option_answer else '-',
        ]
