from .fixtures import (  # noqa: WPS235
    api_v1_document_all,
    inn_fixture,
    mock_fail_face_recognition,
    mock_fail_passport_recognition,
    mock_success_face_recognition,
    mock_success_passport_recognition,
    passport_data,
    passport_fixture,
    registration_fixture,
    selfie_fixture,
    snils_fixture,
)
from .inn import inn_factory, inn_status_accept, inn_status_approval, inn_status_decline
from .passport import passport_factory, passport_status_accept, passport_status_approval, passport_status_decline
from .registration import (
    registration_factory,
    registration_status_accept,
    registration_status_approval,
    registration_status_decline,
)
from .selfie import selfie_factory, selfie_status_accept, selfie_status_approval, selfie_status_decline
from .snils import snils_factory, snils_status_accept, snils_status_approval, snils_status_decline
