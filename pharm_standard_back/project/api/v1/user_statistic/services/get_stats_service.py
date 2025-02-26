import os
import json
import logging
import requests
from datetime import datetime
from uuid import uuid4
from typing import Dict, List
from transliterate import translit

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from matplotlib import pyplot as plt

from apps.helpers.services import AbstractService

logger = logging.getLogger('django')

URL_MONTH = 'http://mskdevserver02.msk.phstd:8001/qvd/month_by_username/?leaders=true'

URL_MULTIPLE_MONTH = (
    'http://mskdevserver02.msk.phstd:8001/qvd/multiple_months_by_username/?month_separately=true&leaders=true'
)


class GetStatsService(AbstractService):
    def __init__(self, serializer_data: Dict, request):
        self.request = request
        self.username = serializer_data.get('username')
        self.date = serializer_data.get('date')

    def _request_for_stats(self, url: str, query_data: Dict) -> Dict:
        """Функция делает запрос за данными, сразу конвертит в json."""
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.post(url, json=query_data, headers=headers)
        if response.status_code != status.HTTP_200_OK:
            raise ValidationError({
                'detail': f'Ошибка при получении данных по пользователю {self.username}, http код ответа != 200',
                'source': url,
                'status': response.status_code,
                's_error': response.status_code,
            })
        return json.loads(response.content.decode('utf-8'))

    def _generate(self, source_data: Dict, scores: List[int], year_data) -> Dict:
        """Распихивает данные и формирует как надо."""
        if not source_data['results']:
            return None

        empl_info = source_data['results'][0]['employee_info']
        prev_month_data = year_data['results'][len(year_data['results']) - 2]['results'][0]['employee_info']

        if empl_info.get('Тип сотрудника') == 'Наладчик':
            rat_1 = '''Общая оценка по Рейтингу за месяц считается как среднее арифметическое всех оценок за смены (СрА) с округлением в большую сторону.
СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к оценке «5».
5 баллов	
Эффективность по КТГ (личная) > чем медиана  + 5%;
3 балла		
Эффективность по КТГ (личная) =  медиана  +/- 5%;
1 балл		
Эффективность по КТГ (личная) < чем медиана  - 5%.

Медиана - значение показателя Эффективность по КТГ  за мес. в среднем по участку.
'''
        elif empl_info.get('Тип сотрудника') == 'Сотрудник бригады':
            rat_1 = '''Общая оценка по Рейтингу за месяц считается как среднее арифметическое всех оценок с учетом стадии производства и номенклатуры (СрА) с округлением в большую сторону. 
СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к оценке «5».
Оценка по номенклатуре:
5 баллов	
Эффективность по OPI по номенклатуре (личная) > чем медиана  + 5%;

3 балла		
Эффективность по OPI (личная) =  медиана  +/- 5%;

1 балл		
Эффективность по OPI (личная) < чем медиана  - 5%.
Медиана - значение показателя Эффективность по OPI за мес. в среднем по участку, с учетом Стадии производства и Номенклатуры.
'''
        elif empl_info.get('Тип сотрудника') == 'Мастер':
            rat_1 = '''Общая оценка по Рейтингу за месяц считается как среднее арифметическое всех оценок с учетом стадии производства и номенклатуры (СрА) с округлением в большую сторону. 
СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к оценке «5».
Оценка по номенклатуре:
5 баллов	
Эффективность по OPI по номенклатуре (личная) > чем медиана  + 5%;
3 балла		
Эффективность по OPI (личная) =  медиана  +/- 5%;
1 балл		
Эффективность по OPI (личная) < чем медиана  - 5%.
Медиана - значение показателя Эффективность по OPI за мес. в среднем по участку, с учетом Стадии производства и Номенклатуры.
'''

        leaders_sector = [item['ФИО'] for item in source_data['results'][0].get('leaders_sector')]
        leaders_plant = [item['ФИО'] for item in source_data['results'][0].get('leaders_plant')]

        if 1 in scores:
            type = 'red'
            assigned_category = 'Особое внимание'
        elif 3 in scores:
            type = 'yellow'
            assigned_category = 'Основа команды'
        else:
            type = 'green'
            assigned_category = 'Лидеры'

        rat_1_increased = None
        prev_rat_1 = prev_month_data['Рейтинг 1.Производительность']
        if prev_rat_1 < empl_info['Рейтинг 1.Производительность']:
            rat_1_increased = True
        elif prev_rat_1 > empl_info['Рейтинг 1.Производительность']:
            rat_1_increased = False
        else:
            rat_1_increased = None

        rat_2_increased = None
        prev_rat_2 = prev_month_data['Рейтинг 2.Качество']
        if prev_rat_2 < empl_info['Рейтинг 2.Качество']:
            rat_2_increased = True
        elif prev_rat_2 > empl_info['Рейтинг 2.Качество']:
            rat_2_increased = False
        else:
            rat_2_increased = None

        rat_3_increased = None
        prev_rat_3 = prev_month_data['Рейтинг 3.Безопасность']
        if prev_rat_3 < empl_info['Рейтинг 3.Безопасность']:
            rat_3_increased = True
        elif prev_rat_3 > empl_info['Рейтинг 3.Безопасность']:
            rat_3_increased = False
        else:
            rat_3_increased = None

        rat_4_increased = None
        prev_rat_4 = prev_month_data['Рейтинг 4.Минимальные простои']
        if prev_rat_4 < empl_info['Рейтинг 4.Минимальные простои']:
            rat_4_increased = True
        elif prev_rat_4 > empl_info['Рейтинг 4.Минимальные простои']:
            rat_4_increased = False
        else:
            rat_4_increased = None

        if empl_info.get('Тип сотрудника') == 'Наладчик':
            performance_indicators_area = [
                {
                    'type': 'personal',
                    'key': 'Эффективность по КТГ (личная)',
                    'value': empl_info['КТГ'],
                    'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Эффективность по КТГ (личная)',
                    'category': [
                        {
                            'type': 'info_type',
                            'name': '',
                            'value': '''
Показатель КТГ (Коэффициент технической готовности), скорректированный на смены, где OPI и КТГ = 0%
'''
                        }
                    ],
                },
                {
                    'type': 'group',
                    'key': 'Эффективность по КТГ (группа)',
                    'value': empl_info['КТГ_Средний_Цех_Участок'],
                },
            ]
        else:
            performance_indicators_area = [
                {
                    'type': 'personal',
                    'key': 'Эффективность по OPI (личная)',
                    'value': empl_info['OPI'],
                    'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Эффективность по OPI (личная)',
                    'category': [
                        {
                            'type': 'info_type',
                            'name': '',
                            'value': '''
Показатель OPI, скорректированный на:

1) время простоев на опытные работы в смену;
2) время санитарных очисток в смену;
3) время простоев на "Нет заказа нет деятельности" в смену;
4) смены, где OPI и КТГ = 0%.
'''
                        }
                    ],
                },
                {
                    'type': 'group',
                    'key': 'Эффективность по OPI (группа)',
                    'value': empl_info['OPI_Средний_Цех_Участок'],
                },
            ]

        rating_data = [
            {
                'name': 'Рейтинг 1. Производительность',
                'value': empl_info['Рейтинг 1.Производительность'],
                'is_increased': rat_1_increased,
                'title_category': 'Критерии отбора в категории',
                'category': [{
                    'type': 'leaders',
                    'name': 'Рейтинг 1. Производительность',
                    'value': rat_1,
                }],
                'detailed_data': []
            },
            {
                'name': 'Рейтинг 2. Качество',
                'value': empl_info['Рейтинг 2.Качество'],
                'is_increased': rat_2_increased,
                'title_category': 'Критерии отбора в категории',
                'category': [{
                    'type': 'leaders',
                    'name': 'Рейтинг 2. Качество',
                    'value': '''СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Рейтинг 2. Качество
Общая оценка по Рейтингу считается как среднее арифметическое всех оценок (СрА) с округлением в большую сторону. СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к оценке «5».
Оценка теоретических знаний пересматривается ежегодно на основе протокола экзамена.
Прочие оценки зависят от фактов депремирований и присваиваются следующим образом:
5 баллов	
Не было депремирований за последний год
3 балла		
Не более 1 депремирования за год
1 балл		
Более 1 депремирования за год
'''
                }],
                'detailed_data': [
                    {
                        'key': '2.1 Теоретические знания по GMP',
                        'value': empl_info['2.1 Теоретические знания по GPM'],
                    },
                    {
                        'key': '2.2 Соблюдение стандартов и процедур',
                        'value': empl_info['2.2 Соблюдение действующих стандар'],
                    },
                    {
                        'key': '2.3 Качество работы',
                        'value': empl_info['2.3 Качество работы: выпускаемой пр'],
                    },
                    {
                        'key': '2.4 Качество ведения документов',
                        'value': empl_info['2.4 ККачество ведения документов (в'],
                    },
                ]
            },
            {
                'name': 'Рейтинг 3. Безопасность',
                'value': empl_info['Рейтинг 3.Безопасность'],
                'is_increased': rat_3_increased,
                'title_category': 'Критерии отбора в категории',
                'category': [{
                    'type': 'leaders',
                    'name': 'Рейтинг 3. Безопасность',
                    'value': '''СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Рейтинг 3. Безопасность

Общая оценка по Рейтингу считается как среднее арифметическое всех оценок (СрА) с округлением в большую сторону. СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к оценке «5».
Оценка теоретических знаний пересматривается ежегодно на основе протокола экзамена.
Прочие оценки зависят от фактов депремирований и присваиваются следующим образом:
5 баллов	
Не было депремирований за последний год
3 балла		
Не более 1 депремирования за год
1 балл		
Более 1 депремирования за год
'''
                }],
                'detailed_data': [
                    {
                        'key': '3.1 Теоретические знания по охране труда (ОТ)',
                        'value': empl_info['3.1 Теоретические знания по охране '],
                    },
                    {
                        'key': '3.2 Соблюдение инструкций по ОТ и ПБ',
                        'value': empl_info['3.2 Соблюдение инструкций по охране'],
                    },
                ]
            },
            {
                'name': 'Рейтинг 4. Дисциплина',
                'value': empl_info['Рейтинг 4.Минимальные простои'],
                'is_increased': rat_4_increased,
                'title_category': 'Критерии отбора в категории',
                'category': [{
                    'type': 'leaders',
                    'name': 'Рейтинг 4. Дисциплина',
                    'value': '''СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Рейтинг 4. Дисциплина
Общая оценка по Рейтингу считается как среднее арифметическое (СрА) с округлением в большую сторону. СрА в диапазоне 2,5-4,49 приводится к оценке «3», СрА ≥ 4,5 приравнивается к «5».
Оценки присваиваются следующим образом:
5 баллов	
Не более 3 дней отпуска за свой счет в год, нет прогулов,	не более 5 дней неявок по болезни в год
3 балла		
4 - 5 дней отпуска за свой счет в год, не более 1 прогула в год, 6–10 дней неявок по болезни в год
1 балл		
Более 5 дней отпуска за свой счет в год, более 1 прогула в год, более 11 дней неявок по болезни в год 
'''
                }],
                'detailed_data': [
                    {'key': '4.1 Дни отпуска за свой счет ', 'value': empl_info['4.1 Дисциплина (дни отпуска за свой ']},
                    {'key': '4.2 Прогулы', 'value': empl_info['4.2 Дисциплина (отсутствие прогулов']},
                    {'key': '4.3 Неявки по болезни', 'value': empl_info['4.3 Неявки по болезни (количество сл']},
                ]
            },
        ]

        genereted_data = {
            'username': source_data['username'],
            'fio': {'key': 'ФИО', 'value': empl_info['ФИО']},
            'service_number': empl_info['Таб. №'],
            'type': {
                'key': translit(empl_info['Тип сотрудника'], 'ru', reversed=True).replace(' ', '_'),
                'value': empl_info['Тип сотрудника'],
            },
            'my_data': [
                {'key': 'Должность', 'value': empl_info['Должность']},
                {'key': 'Тип сотрудника', 'value': empl_info['Тип сотрудника']},
                {'key': 'Наименование завода', 'value': empl_info['Наименование завода']},
                {'key': 'Цех', 'value': empl_info['Цех']},
                {'key': 'Участок', 'value': empl_info['Участок']},
            ],
            'indicators_area': {
                'rating_data': rating_data,
                'plant': source_data['results'][0].get('plant'),
                'leaders_plant': leaders_sector,
                'section': source_data['results'][0].get('section'),
                'charts': [],
                'additional_estimates': [
                    {
                        'type': 'place_rating',
                        'name': 'Место в рейтинге',
                        'value': f"{empl_info['Место в рейтинге участок за месяц']} из {empl_info['Всего сотрудников участок']}",  # noqa: E501
                    },
                    {
                        'type': 'summary_score',
                        'name': 'Сводная оценка',
                        'value': empl_info['Сводная оценка'],
                        'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Сводная оценка',
                        'category': [
                            {
                                'type': 'info_type',
                                'name': '',
                                'value': '''
Единая шкала оценок: 1 (min), 3, 5 (max).

Проекции оценки:
Рейтинг 1.Производительность
Рейтинг 2.Качество
Рейтинг 3.Безопасность
Рейтинг 4.Дисциплина
'''
                            }
                        ],
                    },
                    {
                        'type': type,
                        'name': 'Присвоенная категория',
                        'value': assigned_category,
                        'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Присвоенная категория',
                        'category': [
                            {
                                'type': 'info_type',
                                'name': '',
                                'value': '''
Лидеры			
Все оценки = "5"

Основа команды	
От одной оценки "3", нет ни одной "1"

Особое внимание	
В оценках присутствует хотя бы одна "1" 
'''
                            }
                        ],
                    }
                ],
                'performance_indicators_area': performance_indicators_area,
            },
            'indicators_workshop': {
                'rating_data': rating_data,
                'plant': source_data['results'][0].get('plant'),
                'leaders_plant': leaders_plant,
                'section': source_data['results'][0].get('section'),
                'charts': [],
                'additional_estimates': [
                    {
                        'type': 'place_rating',
                        'name': 'Место в рейтинге',
                        'value': f"{empl_info['Место в рейтинге цех за месяц']} из {empl_info['Всего сотрудников цех']}",  # noqa: E501
                    },
                    {
                        'type': 'summary_score',
                        'name': 'Сводная оценка',
                        'value': empl_info['Сводная оценка'],
                        'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Сводная оценка',
                        'category': [
                            {
                                'type': 'info_type',
                                'name': '',
                                'value': '''
Единая шкала оценок: 1 (min), 3, 5 (max).

Проекции оценки:
Рейтинг 1.Производительность
Рейтинг 2.Качество
Рейтинг 3.Безопасность
Рейтинг 4.Дисциплина
'''
                            }
                        ],
                    },
                    {
                        'type': type,
                        'name': 'Присвоенная категория',
                        'value': assigned_category,
                        'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Присвоенная категория',
                        'category': [
                            {
                                'type': 'info_type',
                                'name': '',
                                'value': '''
Лидеры			
Все оценки = "5"

Основа команды	
От одной оценки "3", нет ни одной "1"

Особое внимание	
В оценках присутствует хотя бы одна "1" 
'''
                            }
                        ],
                    }
                ],
                'performance_indicators_area': performance_indicators_area,
            },
        }
        return genereted_data

    def _generate_chart(self, emp, months_pers, ratings_pers, months_gr, ratings_gr, split) -> Dict:
        if split:
            months_pers = months_pers[-split:]
            ratings_pers = ratings_pers[-split:]
            months_gr = months_gr[-split:]
            ratings_gr = ratings_gr[-split:]

        plt.clf()
        plt.plot(months_pers, ratings_pers)
        plt.plot(months_gr, ratings_gr)
        plt.grid(True)
        chart_path = f'{settings.MEDIA_ROOT}/charts/three_months_{uuid4()}.png'
        plt.savefig(chart_path)
        image = self.request.build_absolute_uri(chart_path)
        if 'http:' in image:
            image = image.replace('http:', 'https:')

        if split == 3:
            type = 'three_months'
        elif split == 6:
            type = 'six_months'
        else:
            type = 'tvelve_months'

        if emp.get('Тип сотрудника') == 'Наладчик':
            performance_indicators_area = [
                {
                    'type': 'personal',
                    'key': 'Эффективность по КТГ (личная)',
                    'value': emp['КТГ'],
                    'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Эффективность по КТГ (личная)',
                    'category': [
                        {
                            'type': 'info_type',
                            'name': '',
                            'value': '''
Показатель КТГ (Коэффициент технической готовности), скорректированный на смены, где OPI и КТГ = 0%
'''
                        }
                    ],
                },
                {
                    'type': 'group',
                    'key': 'Эффективность по КТГ (группа)',
                    'value': emp['КТГ_Средний_Цех_Участок'],
                },
            ]
        else:
            performance_indicators_area = [
                {
                    'type': 'personal',
                    'key': 'Эффективность по OPI (личная)',
                    'value': emp['OPI'],
                    'title_category': 'СПРАВКА ДЛЯ ПОКАЗАТЕЛЯ Эффективность по OPI (личная)',
                    'category': [
                        {
                            'type': 'info_type',
                            'name': '',
                            'value': '''
Показатель OPI, скорректированный на:

1) время простоев на опытные работы в смену;
2) время санитарных очисток в смену;
3) время простоев на "Нет заказа нет деятельности" в смену;
4) смены, где OPI и КТГ = 0%.
'''
                        }
                    ],
                },
                {
                    'type': 'group',
                    'key': 'Эффективность по OPI (группа)',
                    'value': emp['OPI_Средний_Цех_Участок'],
                },
            ]

        return {
            'performance_indicators': performance_indicators_area,
            'type': type,
            'image': image,
        }

    def _genereate_charts(self, emp_info: Dict, year_data: Dict) -> List:
        if not year_data or not year_data['results']:
            return []

        if not os.path.exists(f'{settings.MEDIA_ROOT}/charts'):
            os.mkdir(f'{settings.MEDIA_ROOT}/charts')

        performances_list_personal = []
        performances_list_workshop = []
        performances_list_area = []

        for result in year_data.get('results'):
            for subresult in result.get('results'):
                if subresult.get('employee_info').get('Тип сотрудника') in ('Сотрудник бригады', 'Мастер'):
                    performances_list_personal.append(
                        (
                            float(subresult.get('employee_info').get('OPI')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )
                    performances_list_workshop.append(
                        (
                            float(subresult.get('employee_info').get('OPI_Средний_Цех_Участок')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )
                    performances_list_area.append(
                        (
                            float(subresult.get('employee_info').get('OPI_Средний_Цех')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )
                elif subresult.get('employee_info').get('Тип сотрудника') == 'Наладчик':
                    performances_list_personal.append(
                        (
                            float(subresult.get('employee_info').get('КТГ')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )
                    performances_list_workshop.append(
                        (
                            float(subresult.get('employee_info').get('КТГ_Средний_Цех_Участок')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )
                    performances_list_area.append(
                        (
                            float(subresult.get('employee_info').get('КТГ_Средний_Цех')) * 100,
                            subresult.get('employee_info').get('Месяц')
                        )
                    )

        months_personal = [item[1] for item in performances_list_personal]
        ratings_personal = [item[0] for item in performances_list_personal]

        months_workshop = [item[1] for item in performances_list_workshop]
        ratings_workshop = [item[0] for item in performances_list_workshop]

        months_group_area = [item[1] for item in performances_list_area]
        ratings_group_area = [item[0] for item in performances_list_area]

        three_workshop = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_workshop,
            ratings_gr=ratings_workshop,
            split=3,
        )
        three_area = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_group_area,
            ratings_gr=ratings_group_area,
            split=3,
        )
        six_workshop = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_workshop,
            ratings_gr=ratings_workshop,
            split=6,
        )
        six_area = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_group_area,
            ratings_gr=ratings_group_area,
            split=6,
        )
        tvelve_workshop = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_workshop,
            ratings_gr=ratings_workshop,
            split=None,
        )
        tvelve_area = self._generate_chart(
            emp=emp_info,
            months_pers=months_personal,
            ratings_pers=ratings_personal,
            months_gr=months_group_area,
            ratings_gr=ratings_group_area,
            split=None,
        )
        return [[three_workshop, six_workshop, tvelve_workshop], [three_area, six_area, tvelve_area]]

    def process(self):
        # Первый запрос, за текущий месяц
        month_data = self._request_for_stats(url=URL_MONTH, query_data={'username': self.username, 'date': self.date})

        # Второй запрос, за год, для агрегации нужных данных и построения графиков
        curr_year, curr_month = datetime.now().strftime('%Y-%m').split('-')
        start_period = f'{int(curr_year) - 1}-{curr_month}-01'
        end_period = f'{curr_year}-{curr_month}-28'
        year_data = self._request_for_stats(
            url=URL_MULTIPLE_MONTH,
            query_data={'username': self.username, 'start_period': start_period, 'end_period': end_period},
        )

        # Собрать данные по году из оценок рейтингов для присвоения категории
        scores = []
        for result in month_data.get('results'):
            scores.append(int(result.get('employee_info').get('Рейтинг 1.Производительность')))
            scores.append(int(result.get('employee_info').get('Рейтинг 2.Качество')))
            scores.append(int(result.get('employee_info').get('Рейтинг 3.Безопасность')))
            scores.append(int(result.get('employee_info').get('Рейтинг 4.Минимальные простои')))

        # Генерирует json с данными, без графиков
        genereted_data = self._generate(source_data=month_data, scores=scores, year_data=year_data)
        if not genereted_data:
            return []

        # Отдельно сформировать графики за месяц, полгода, год
        emp_info = month_data['results'][0]['employee_info']
        charts = self._genereate_charts(emp_info=emp_info, year_data=year_data)
        genereted_data['indicators_area']['charts'] = charts[1]
        genereted_data['indicators_workshop']['charts'] = charts[0]

        return genereted_data
