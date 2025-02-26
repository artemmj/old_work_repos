import pytest

from apps.helpers.sms import RedSmsService


@pytest.mark.django_db
def test_red_sms_200_ok(mock_200_redsms):
    assert RedSmsService(phone='', message='').process()


@pytest.mark.django_db
def test_red_sms_400_bad(mock_400_redsms):
    assert not RedSmsService(phone='', message='').process()
