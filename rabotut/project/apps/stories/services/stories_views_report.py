import structlog
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font

from apps.departments.models import Department
from apps.helpers.services import AbstractService
from apps.stories.models import Stories, StoriesRead

log = structlog.getLogger()


class StoriesViewsReportService(AbstractService):
    def __init__(self, start: str, end: str) -> None:
        self.start_date = start
        self.end_date = end
        self.wb = Workbook()
        self.ws = self.wb.active

    def process(self) -> Workbook:
        """Генерация отчета по просмотрам сторис, возвращает книгу xlsx (Workbook)."""
        self._write_headers()
        total_counter = self._write_stories_data()
        self._write_total_cells(total_counter=total_counter)
        return self.wb

    def _write_headers(self):
        """Проставить хедеры, все заведенные в БД департаменты."""
        self.ws.column_dimensions['A'].width = 22
        departments = Department.objects.non_deleted()
        first_cell = WriteOnlyCell(self.ws, value='Сторис')
        first_cell.font = Font(bold=True)

        cells = [first_cell]
        for depart in departments:
            cell = WriteOnlyCell(self.ws, value=depart.name)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='right')
            cells.append(cell)

        last_cell = WriteOnlyCell(self.ws, value='Всего')
        last_cell.alignment = Alignment(horizontal='right')
        last_cell.font = Font(bold=True)
        cells.append(last_cell)
        self.ws.append(cells)

    def _write_stories_data(self) -> int:
        """Записывает данные по просмотрам по каждой сторис в каждом департаменте."""
        total_counter = 0  # для хранения кол-ва всех просмотров всех сторис
        for stori in Stories.objects.all():
            internal_total_counter = 0    # для хранения кол-ва всех просмотров конкретной сторис
            stories_cells = [stori.name]

            for depart in Department.objects.non_deleted():
                counter = self._read_stories_counter(stori, depart)
                internal_total_counter += counter
                stories_cells.append(WriteOnlyCell(self.ws, value=counter))

            total_counter += internal_total_counter
            stories_cells.append(WriteOnlyCell(self.ws, value=internal_total_counter))
            self.ws.append(stories_cells)
        return total_counter

    def _read_stories_counter(self, stories: Stories, department: str) -> int:
        """Счетчик просмотренных сторис."""
        return StoriesRead.objects.filter(
            created_at__date__gte=self.start_date,
            created_at__date__lte=self.end_date,
            stories=stories,
            user__department=department,
        ).count()

    def _write_total_cells(self, total_counter: int) -> None:
        """Записать последнюю строку Итого."""
        total_value_cell = WriteOnlyCell(self.ws, value=total_counter)
        total_value_cell.font = Font(bold=True)
        deps_count = Department.objects.non_deleted().count()
        # Нужно сместить колонку Итого на количество департаментов
        cell = ['' for _ in range(deps_count)]
        total_cell = WriteOnlyCell(self.ws, value='Итого')
        total_cell.font = Font(bold=True)
        total_cell.alignment = Alignment(horizontal='right')
        cell.append(total_cell)
        cell.append(total_value_cell)
        self.ws.append(cell)
