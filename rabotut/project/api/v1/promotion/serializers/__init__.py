from .promotion import (
    PromotionCreateSerializer,
    PromotionListIdSerializer,
    PromotionRetrieveSerializer,
    PromotionSerializer,
    PromotionUpdateSerializer,
)
from .promotion_emoji import PromotionEmojiPostSerializer, PromotionEmojiSerializer
from .promotion_mailing import (  # noqa: WPS235
    BasePromotionMailingListSerializer,
    BasePromotionMailingSerializer,
    PromotionMailingDepartmentRetrieveSerializer,
    PromotionMailingDepartmentSerializer,
    PromotionMailingPolymorphicSerializer,
    PromotionMailingProjectRetrieveSerializer,
    PromotionMailingProjectSerializer,
    PromotionMailingRegionRetrieveSerializer,
    PromotionMailingRegionSerializer,
    PromotionMailingRetrievePolymorphicSerializer,
    PromotionMailingRetrieveSwaggerSerializer,
    PromotionMailingSwaggerSerializer,
    PromotionMailingUpdateSwaggerSerializer,
    PromotionMailingUserRoleRetrieveSerializer,
    PromotionMailingUserRoleSerializer,
)
from .promotion_mobile import PromotionMobileRetrieveSerializer, PromotionMobileSerializer
