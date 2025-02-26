from .check_docs import CheckDocResponseSerializer
from .documents import (  # noqa: WPS235
    BankDetailSerializer,
    DocumentAllArketaSerializer,
    EmailArketaReadSerializer,
    EmailArketaWriteSerializer,
    InnArketaReadSerializer,
    InnArketaWriteSerializer,
    RegistrationArketaReadSerializer,
    RegistrationArketaWriteSerializer,
    SelfieArketaReadSerializer,
    SelfieArketaWriteSerializer,
    SnilsArketaReadSerializer,
    SnilsArketaWriteSerializer,
    SpreadArketaReadSerializer,
    SpreadArketaWriteSerializer,
)
from .file import FileArketaExtendedSerializer, FileArketaUploadSerializer
from .task import (  # noqa: WPS235
    FeedbackArketaMobileReadSerializer,
    TaskArketaAnswerWriteRequestSerializer,
    TaskArketaCancelReservationSerializer,
    TaskArketaCurrentQuerySerializer,
    TaskArketaFeedbackCompactSerializer,
    TaskArketaFeedbackSerializer,
    TaskArketaMobileCompactSerializer,
    TaskArketaMobileSerializer,
    TaskArketaReserveCounterSerializer,
    TaskArketaStatusesSerializer,
    TaskArketaTakeSerializer,
    TaskArketaVacantQuerySerializer,
    TaskArketaVacantSerializer,
)
from .trade_point import TradePointArketaVacantQuerySerializer, TradePointArketaVacantSerializer
from .visit import VisitArketaResponseSerializer, VisitArketaSerializer
