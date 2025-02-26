import urllib

import httpx
import pytest
from django.conf import settings


@pytest.fixture
def mock_200_arketa_trade_point_vacant(respx_mock):
    """Мок 200 ответа апи аркеты trade_point_vacant."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}trade_point/vacant/?distance__latitude=55.755819&distance__longitude=37.617644&limit=50'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_trade_point_vacant(respx_mock):
    """Мок 400 ответа апи аркеты trade_point_vacant."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}trade_point/vacant/?distance__latitude=55.755819&distance__longitude=37.617644&limit=50'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_task_vacant(respx_mock):
    """Мок 200 ответа апи аркеты task_vacant."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/vacant/?distance__latitude=55.755819&distance__longitude=37.617644&trade_point=tp'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_task_vacant(respx_mock):
    """Мок 400 ответа апи аркеты task_vacant."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/vacant/?distance__latitude=55.755819&distance__longitude=37.617644&trade_point=tp'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_task_available_for_reserve(respx_mock):
    """Мок 200 ответа апи аркеты task_available_for_reserve."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/available_for_reserve/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_task_available_for_reserve(respx_mock):
    """Мок 400 ответа апи аркеты task_available_for_reserve."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/available_for_reserve/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_task_preview(respx_mock):
    """Мок 200 ответа апи аркеты task_preview."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/abc/preview/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_task_preview(respx_mock):
    """Мок 400 ответа апи аркеты task_preview."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/abc/preview/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_vacant_take(respx_mock):
    """Мок 200 ответа апи аркеты vacant_take."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/vacant/take/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_vacant_take(respx_mock):
    """Мок 400 ответа апи аркеты vacant_take."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/vacant/take/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_change_user_phone(respx_mock):
    """Мок 200 ответа апи аркеты на смену номера телефона."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/abc/phone/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_change_user_phone(respx_mock):
    """Мок 400 ответа апи аркеты на смену номера телефона."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/abc/phone/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_201_arketa_create_user(respx_mock):
    """Мок 201 ответа апи аркеты на создание юзера."""
    response = httpx.Response(201, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/registration/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_create_user(respx_mock):
    """Мок 400 ответа апи аркеты на создание юзера."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/registration/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_check_user_exists(respx_mock):
    """Мок 200 ответа апи аркеты на проверку юзера."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/exists/?'
    url += urllib.parse.urlencode({'phone': '+79000000000'})
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_check_user_exists(respx_mock):
    """Мок 400 ответа апи аркеты на проверку юзера."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/exists/?'
    url += urllib.parse.urlencode({'phone': '+79000000000'})
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_check_docs(respx_mock):
    """Мок 200 ответа апи аркеты на проверку документов."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/check_docs/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_check_docs(respx_mock):
    """Мок 400 ответа апи аркеты на проверку документов."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/check_docs/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_get_documents(respx_mock):
    """Мок 200 ответа апи аркеты на получение документов."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/documents/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_get_documents(respx_mock):
    """Мок 400 ответа апи аркеты на получение документов."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/documents/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_email(respx_mock):
    """Мок 200 ответа апи аркеты на изменение эл. почты."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/email/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_email(respx_mock):
    """Мок 400 ответа апи аркеты на изменение эл. почты."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/email/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_inn(respx_mock):
    """Мок 200 ответа апи аркеты на изменение ИНН."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/inn/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_inn(respx_mock):
    """Мок 400 ответа апи аркеты на изменение ИНН."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/inn/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_registration(respx_mock):
    """Мок 200 ответа апи аркеты на изменение регистрации."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/registration/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_registration(respx_mock):
    """Мок 400 ответа апи аркеты на изменение регистрации."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/registration/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_selfie(respx_mock):
    """Мок 200 ответа апи аркеты на изменение селфи."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/selfie/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_selfie(respx_mock):
    """Мок 400 ответа апи аркеты на изменение селфи."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/selfie/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_snils(respx_mock):
    """Мок 200 ответа апи аркеты на изменение СНИЛС."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/snils/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_snils(respx_mock):
    """Мок 400 ответа апи аркеты на изменение СНИЛС."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/snils/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_spread(respx_mock):
    """Мок 200 ответа апи аркеты на изменение разворота."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/spread/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_spread(respx_mock):
    """Мок 400 ответа апи аркеты на изменение разворота."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/document/user/user_id/spread/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_statuses(respx_mock):
    """Мок 200 ответа апи аркеты на статусы документов."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/statuses/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_statuses(respx_mock):
    """Мок 400 ответа апи аркеты на статусы документов."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/statuses/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_current(respx_mock):
    """Мок 200 ответа апи аркеты на текущие задачи."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/current/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_current(respx_mock):
    """Мок 400 ответа апи аркеты на текущие задачи."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/current/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_cancel_reservation(respx_mock):
    """Мок 200 ответа апи аркеты на отмену брони."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/cancel_reservation/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_cancel_reservation(respx_mock):
    """Мок 400 ответа апи аркеты на отмену брони."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/cancel_reservation/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_answer(respx_mock):
    """Мок 200 ответа апи аркеты на ответ."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/answer/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_answer(respx_mock):
    """Мок 400 ответа апи аркеты на ответ."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/answer/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_visit(respx_mock):
    """Мок 200 ответа апи аркеты на визит точки."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}visit/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_visit(respx_mock):
    """Мок 400 ответа апи аркеты на визит точки."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}visit/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_get_file(respx_mock):
    """Мок 200 ответа апи аркеты на получение файла."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/file_id/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_get_file(respx_mock):
    """Мок 400 ответа апи аркеты на получение файла."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/file_id/'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_create_file(respx_mock):
    """Мок 200 ответа апи аркеты на создание файла."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_create_file(respx_mock):
    """Мок 400 ответа апи аркеты на создание файла."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_put_file(respx_mock):
    """Мок 200 ответа апи аркеты на PUT файла."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_put_file(respx_mock):
    """Мок 400 ответа апи аркеты на PUT файла."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.put(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_patch_file(respx_mock):
    """Мок 200 ответа апи аркеты на PATCH файла."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.patch(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_patch_file(respx_mock):
    """Мок 400 ответа апи аркеты на PATCH файла."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.patch(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_delete_file(respx_mock):
    """Мок 200 ответа апи аркеты на DELETE файла."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.delete(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_delete_file(respx_mock):
    """Мок 400 ответа апи аркеты на DELETE файла."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}file/abc/'
    respx_mock.delete(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_feedback_notifications(respx_mock):
    """Мок 200 ответа апи аркеты на фидбек."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/notifications/?'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_feedback_notifications(respx_mock):
    """Мок 400 ответа апи аркеты на фидбек."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/notifications/?'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_feedback_create(respx_mock):
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_feedback_create(respx_mock):
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_feedback_show_to_executor(respx_mock):
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/abc/show_to_executor/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_feedback_show_to_executor(respx_mock):
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}feedback/abc/show_to_executor/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_like(respx_mock):
    """Мок 200 ответа апи аркеты на лайк задачи."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/like/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_like(respx_mock):
    """Мок 400 ответа апи аркеты на лайк задачи."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/like/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_200_arketa_dislike(respx_mock):
    """Мок 200 ответа апи аркеты на лайк задачи."""
    response = httpx.Response(200, content=b'{"results": true}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/dislike/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_400_arketa_dislike(respx_mock):
    """Мок 400 ответа апи аркеты на лайк задачи."""
    response = httpx.Response(400, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}task/task_id/dislike/'
    respx_mock.post(url).mock(return_value=response)


@pytest.fixture
def mock_500_arketa_api_client_trade_point_vacant(respx_mock):
    """Мок 500 ответа апи аркеты trade_point_vacant."""
    response = httpx.Response(500, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}trade_point/vacant/?distance__latitude=55.755819&distance__longitude=37.617644&limit=50'
    respx_mock.get(url).mock(return_value=response)


@pytest.fixture
def mock_500_arketa_service_api_client_create_user(respx_mock):
    """Мок 500 ответа сервисного апи аркеты create_user."""
    response = httpx.Response(500, content=b'{"results": false}')
    api_url = f'{settings.ARKETA_API_URL}api/v4/'
    url = f'{api_url}rabotut/user/registration/'
    respx_mock.post(url).mock(return_value=response)
