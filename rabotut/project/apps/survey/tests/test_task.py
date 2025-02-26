import pytest
from apps.survey.services import SurveyReportService


@pytest.mark.django_db
def test_survey_report(answer, survey):
    wb = SurveyReportService().process(str(survey.id))
    assert wb != None
