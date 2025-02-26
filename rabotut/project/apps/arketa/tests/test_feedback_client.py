import pytest

from rest_framework.exceptions import ValidationError

from apps.arketa.clients import ArketaFeedbackApiClient



@pytest.mark.django_db
def test_feedback_api_client_notifications(mock_200_arketa_feedback_notifications):
    result = ArketaFeedbackApiClient('abc').notifications({})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_feedback_api_client_notifications(mock_400_arketa_feedback_notifications):
    with pytest.raises(ValidationError):
        result = ArketaFeedbackApiClient('abc').notifications({})
        assert not result.get('results')


@pytest.mark.django_db
def test_feedback_api_client_create(mock_200_arketa_feedback_create):
    result = ArketaFeedbackApiClient('abc').create({})
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_feedback_api_client_create(mock_400_arketa_feedback_create):
    with pytest.raises(ValidationError):
        result = ArketaFeedbackApiClient('abc').create({})
        assert not result.get('results')


@pytest.mark.django_db
def test_feedback_api_client_show_to_executor(mock_200_arketa_feedback_show_to_executor):
    result = ArketaFeedbackApiClient('abc').show_to_executor('abc')
    assert result.get('results')


@pytest.mark.django_db
def test_fail_400_feedback_api_client_show_to_executor(mock_400_arketa_feedback_show_to_executor):
    with pytest.raises(ValidationError):
        result = ArketaFeedbackApiClient('abc').show_to_executor('abc')
        assert not result.get('results')
