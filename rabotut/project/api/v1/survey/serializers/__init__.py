from .answer import AnswerCreateSerializer, AnswerSerializer
from .option import OptionCreateSerializer, OptionSerializer
from .question import QuestionCreateSerializer, QuestionSerializer
from .survey import (
    SurveyCreateSerializer,
    SurveyListIdSerializer,
    SurveyRetrieveSerializer,
    SurveySerializer,
    SurveyUpdateSerializer,
)
from .survey_mailing import (  # noqa: WPS235
    BaseSurveyMailingListSerializer,
    BaseSurveyMailingSerializer,
    SurveyMailingDepartmentRetrieveSerializer,
    SurveyMailingDepartmentSerializer,
    SurveyMailingPolymorphicSerializer,
    SurveyMailingProjectRetrieveSerializer,
    SurveyMailingProjectSerializer,
    SurveyMailingRegionRetrieveSerializer,
    SurveyMailingRegionSerializer,
    SurveyMailingRetrievePolymorphicSerializer,
    SurveyMailingUserRoleRetrieveSerializer,
    SurveyMailingUserRoleSerializer,
)
from .survey_mobile import SendSurveyReplySerializer, SurveyMobileRetrieveSerializer, SurveyMobileSerializer
from .swagger import (
    SurveyMailingRetrieveSwaggerSerializer,
    SurveyMailingSwaggerSerializer,
    SurveyMailingUpdateSwaggerSerializer,
)
