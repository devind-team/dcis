from typing import Any

import graphene
from django.db.models import Prefetch
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from django.db.models import QuerySet
from graphene import ConnectionField
from graphene_django import DjangoListField
from graphql import ResolveInfo
from graphql_relay import from_global_id
from stringcase import snakecase

from devind_helpers.utils import gid2int

from apps.core.models import User
from apps.core.schema import UserType
from apps.core.services.user_services import get_user_from_id_or_context
from apps.dcis.helpers.info_fields import get_fields
from apps.dcis.models import AttributeValue, CuratorGroup, Period, Privilege, Sheet, Attribute, Document
from apps.dcis.permissions import can_change_period_sheet, can_view_period
from apps.dcis.schema.types import (
    CuratorGroupType,
    DivisionModelTypeConnection,
    PeriodType,
    PrivilegeType,
    SheetType,
    AttributeType,
    AttributeValueType,
)
from apps.dcis.services.divisions_services import get_period_possible_divisions
from apps.dcis.services.period_services import (
    get_period_users,
    get_user_period_privileges,
    get_user_periods,
    get_period_attributes,
)
from apps.dcis.services.sheet_unload_services import DocumentsSheetUnloader


class CuratorGroupQueries(graphene.ObjectType):
    """Запросы записей, связанных с группами кураторов."""

    curator_group: CuratorGroup = DjangoListField(
        CuratorGroupType,
        required=True,
        description='Кураторская группа'
    )
