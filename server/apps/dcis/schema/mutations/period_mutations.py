from typing import Any

import graphene
from devind_core.models import File
from devind_helpers.decorators import permission_classes
from devind_helpers.exceptions import PermissionDenied
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation, DjangoUpdateMutation
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Division, Period, PeriodGroup, PeriodPrivilege, Privilege, Project
from apps.dcis.permissions import (
    AddPeriod,
    DeletePeriod,
    ChangePeriodDivisions,
    ChangePeriodGroups,
    ChangePeriodSettings,
    ChangePeriodUsers,
    ViewPeriod,
)
from apps.dcis.schema.types import DivisionModelType, PeriodGroupType, PeriodType, PrivilegeType
from apps.dcis.services.divisions_services import get_divisions
from apps.dcis.services.excel_extractor_services import ExcelExtractor
from apps.dcis.services.period_services import (
    create_period,
    add_period_methodical_support,
    add_divisions_period,
    remove_divisions_period,
    copy_period_groups,
    change_period_group_privileges,
    change_user_period_groups,
    change_user_period_privileges
)


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='Xlsx файл с проектом')
        multiple = graphene.Boolean(required=True, description='Множественность сбора')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated, AddPeriod,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        name: str,
        project_id: str,
        file: InMemoryUploadedFile,
        multiple: bool
    ):
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        info.context.check_object_permissions(info.context, project)
        period: Period = create_period(name, info.context.user, project, multiple)
        fl: File = add_period_methodical_support(period, file, info.context.user)
        extractor: ExcelExtractor = ExcelExtractor(fl.src.path)
        extractor.save(period)
        return AddPeriodMutation(period=period)


class ChangePeriodMutationPayload(DjangoCudBaseMutation, DjangoUpdateMutation):
    """Мутация на изменение настроек периода."""

    class Meta:
        model = Period
        login_required = True
        exclude_fields = ('project', 'methodical_support',)
        optional_fields = ('start', 'expiration', 'user',)

    period = graphene.Field(PeriodType, description='Измененный период')

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, input: Any, id: str, obj: Period) -> None:
        if not ChangePeriodSettings.has_object_permission(info.context, obj):
            raise PermissionDenied('Ошибка доступа')


class DeletePeriodMutation(BaseMutation):
    """Мутация на удаление периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного периода')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodSettings,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str):
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        period.delete()
        return DeletePeriodMutation(delete_id=period_id)


class AddDivisionsMutation(BaseMutation):
    """Мутация на добавление дивизионов в период."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы дивизионов')

    divisions = graphene.List(DivisionModelType, required=True, description='Новые дивизионы')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodDivisions,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_ids: list[str]):
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        return AddDivisionsMutation(divisions=add_divisions_period(period, division_ids))


class DeleteDivisionMutation(BaseMutation):
    """Мутация на удаление дивизиона из периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_id = graphene.ID(required=True, description='Идентификатор дивизиона')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного дивизиона')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodDivisions,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_id: str):
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        remove_divisions_period(period_id, division_id)
        return DeleteDivisionMutation(delete_id=division_id)


class AddPeriodGroupMutationPayload(DjangoCudBaseMutation, DjangoCreateMutation):
    """Мутация на добавление группы периода."""

    class Meta:
        model = PeriodGroup
        login_required = True
        exclude_fields = ('users', 'privileges',)

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, input: Any) -> None:
        period = get_object_or_404(Period, pk=input.period)
        if not ChangePeriodGroups.has_object_permission(info.context, period):
            raise PermissionDenied('Ошибка доступа')


class CopyPeriodGroupsMutation(BaseMutation):
    """Мутация на перенос групп с пользователями из другого периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор текущего периода')
        selected_period_id = graphene.ID(required=True, description='Идентификатор выбранного периода')
        period_group_ids = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Выбранные группы')

    period_groups = graphene.List(PeriodGroupType, required=True, description='Новые группы периода')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodGroups,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        selected_period_id: str,
        period_group_ids: list[str]
    ):
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        selected_period = get_object_or_404(Period, pk=selected_period_id)
        if not ViewPeriod.has_object_permission(info.context, selected_period):
            raise PermissionDenied('Ошибка доступа')
        return CopyPeriodGroupsMutation(period_groups=copy_period_groups(period_group_ids, period, selected_period))


class ChangePeriodGroupPrivilegesMutation(BaseMutation):
    """Мутация на изменение привилегий группы."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')
        privileges_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы привилегий')

    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии группы')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodGroups,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: int, privileges_ids: list[str]):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        info.context.check_object_permissions(info.context, period_group.period)
        return ChangePeriodGroupPrivilegesMutation(privileges=change_period_group_privileges(privileges_ids,
                                                                                             period_group))


class DeletePeriodGroupMutation(BaseMutation):
    """Мутация на удаление группы периода."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленной группы периода')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodGroups,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: str):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        info.context.check_object_permissions(info.context, period_group.period)
        period_group.delete()
        return DeletePeriodMutation(delete_id=period_group_id)


class ChangeUserPeriodGroupsMutation(BaseMutation):
    """Мутация на изменение групп пользователя в периоде."""

    class Input:
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')
        period_group_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            description='Идентификаторы групп пользователя в периоде'
        )

    user = graphene.Field(UserType, required=True, description='Пользователь')
    period_groups = graphene.List(PeriodGroupType, required=True, description='Группы пользователя')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodUsers,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_group_ids: list[PeriodGroup]):
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        user.periodgroup_set.set(change_user_period_groups(period_group_ids, info))
        return ChangeUserPeriodGroupsMutation(
            user=user,
            period_groups=change_user_period_groups(period_group_ids, info)
        )


class ChangeUserPeriodPrivilegesMutation(BaseMutation):
    """Мутация на изменение отдельных привилегий пользователя в периоде."""

    class Input:
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        privileges_ids = graphene.List(
            graphene.NonNull(graphene.ID),
            description='Идентификаторы привилегий пользователя в периоде'
        )

    user = graphene.Field(UserType, required=True, description='Пользователь')
    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии пользователя в периоде')

    @staticmethod
    @permission_classes((IsAuthenticated, ChangePeriodUsers,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_id: str, privileges_ids: list[str]):
        period = get_object_or_404(Period, pk=period_id)
        info.context.check_object_permissions(info.context, period)
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        return ChangeUserPeriodPrivilegesMutation(
            user=user,
            privileges=change_user_period_privileges(user.id,
                                                     period.id,
                                                     privileges_ids)
        )


class PeriodMutations(graphene.ObjectType):
    """Список мутация периода."""

    add_period = AddPeriodMutation.Field(required=True)
    change_period = ChangePeriodMutationPayload.Field(required=True)
    delete_period = DeletePeriodMutation.Field(required=True)

    add_divisions = AddDivisionsMutation.Field(required=True)
    delete_division = DeleteDivisionMutation.Field(required=True)

    add_period_group = AddPeriodGroupMutationPayload.Field(required=True)
    copy_period_groups = CopyPeriodGroupsMutation.Field(required=True)
    change_period_group_privileges = ChangePeriodGroupPrivilegesMutation.Field(required=True)
    delete_period_group = DeletePeriodGroupMutation.Field(required=True)

    change_user_period_groups = ChangeUserPeriodGroupsMutation.Field(required=True)
    change_user_period_privileges = ChangeUserPeriodPrivilegesMutation.Field(required=True)
