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
    can_add_period,
    can_change_period_divisions,
    can_change_period_groups,
    can_change_period_settings,
    can_change_period_users,
    can_view_period,
)
from apps.dcis.schema.types import DivisionModelType, PeriodGroupType, PeriodType, PrivilegeType
from apps.dcis.services.divisions_services import get_divisions
from apps.dcis.services.excel_extractor_services import ExcelExtractor


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='Xlsx файл с проектом')
        multiple = graphene.Boolean(required=True, description='Множественность сбора')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        name: str,
        project_id: str,
        file: InMemoryUploadedFile,
        multiple: bool
    ):
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        can_add_period(info.context, project)
        period: Period = Period.objects.create(
            name=name,
            user=info.context.user,
            project=project,
            multiple=multiple
        )
        fl: File = period.methodical_support.create(
            name=file.name,
            src=file,
            deleted=False,
            user=info.context.user
        )
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
        can_change_period_settings(info.context, obj)


class DeletePeriodMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление периода."""

    class Meta:
        model = Period
        login_required = True

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, id: str, obj: Period) -> None:
        can_change_period_settings(info.context, obj)


class AddDivisionsMutation(BaseMutation):
    """Мутация на добавление дивизионов в период."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы дивизионов')

    divisions = graphene.List(DivisionModelType, required=True, description='Новые дивизионы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_ids: list[str]):
        period = get_object_or_404(Period, pk=period_id)
        can_change_period_divisions(info.context, period)
        division_links = Division.objects.bulk_create([
            Division(period=period, object_id=division_id) for division_id in division_ids
        ])
        divisions = period.project.division.objects.filter(pk__in=[link.object_id for link in division_links])
        return AddDivisionsMutation(divisions=get_divisions(divisions))


class DeleteDivisionMutation(BaseMutation):
    """Мутация на удаление дивизиона из периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_id = graphene.ID(required=True, description='Идентификатор дивизиона')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного дивизиона')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_id: str):
        period = get_object_or_404(Period, pk=period_id)
        can_change_period_divisions(info.context, period)
        Division.objects.get(period_id=period_id, object_id=division_id).delete()
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
        can_change_period_groups(info.context, period)


class CopyPeriodGroupsMutation(BaseMutation):
    """Мутация на перенос групп с пользователями из другого периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор текущего периода')
        selected_period_id = graphene.ID(required=True, description='Идентификатор выбранного периода')
        period_group_ids = graphene.List(graphene.NonNull(graphene.ID), required=True, description='Выбранные группы')

    period_groups = graphene.List(PeriodGroupType, required=True, description='Новые группы периода')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        selected_period_id: str,
        period_group_ids: list[str]
    ):
        period = get_object_or_404(Period, pk=period_id)
        can_change_period_groups(info.context, period)
        selected_period = get_object_or_404(Period, pk=selected_period_id)
        can_view_period(info.context, selected_period)
        period_groups: list[PeriodGroup] = []
        for period_group_id in period_group_ids:
            period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
            period_groups.append(period_group)
            new_group = PeriodGroup.objects.create(name=period_group.name, period=period)
            new_group.users.set(period_group.users.all())
            new_group.privileges.set(period_group.privileges.all())
            for user in period_group.users.all():
                for period_privilege in user.periodprivilege_set.filter(period=selected_period).all():
                    PeriodPrivilege.objects.create(period=period, user=user, privilege=period_privilege.privilege)
        return CopyPeriodGroupsMutation(period_groups=period_groups)


class ChangePeriodGroupPrivilegesMutation(BaseMutation):
    """Мутация на изменение привилегий группы."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')
        privileges_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы привилегий')

    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: int, privileges_ids: list[str]):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        can_change_period_groups(info.context, period_group.period)
        privileges: list[Privilege] = []
        for privilege_id in privileges_ids:
            privilege = get_object_or_404(Privilege, pk=privilege_id)
            privileges.append(privilege)
        period_group.privileges.set(privileges)
        return ChangePeriodGroupPrivilegesMutation(privileges=privileges)


class DeletePeriodGroupMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление группы периода."""

    class Meta:
        model = PeriodGroup
        login_required = True

    @classmethod
    def check_permissions(cls, root: Any, info: ResolveInfo, id: str, obj: PeriodGroup) -> None:
        can_change_period_groups(info.context, obj.period)


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
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_group_ids: list[PeriodGroup]):
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        period_groups: list[PeriodGroup] = []
        for period_group_id in period_group_ids:
            period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
            can_change_period_users(info.context, period_group.period)
            period_groups.append(period_group)
        user.periodgroup_set.set(period_groups)
        return ChangeUserPeriodGroupsMutation(user=user, period_groups=period_groups)


class ChangeUserPeriodPrivileges(BaseMutation):
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
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_id: str, privileges_ids: list[str]):
        period = get_object_or_404(Period, pk=period_id)
        can_change_period_users(info.context, period)
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        PeriodPrivilege.objects.filter(period_id=period.id, user_id=user.id).delete()
        privileges: list[Privilege] = []
        for privileges_id in privileges_ids:
            privilege = get_object_or_404(Privilege, pk=privileges_id)
            PeriodPrivilege.objects.create(period_id=period.id, user_id=user.id, privilege=privilege)
            privileges.append(privilege)
        return ChangeUserPeriodPrivileges(user=user, privileges=privileges)


class PeriodMutations(graphene.ObjectType):
    """Список мутация периода."""

    add_period = AddPeriodMutation.Field(required=True)
    change_period = ChangePeriodMutationPayload.Field(required=True)
    delete_period = DeletePeriodMutationPayload.Field(required=True)

    add_divisions = AddDivisionsMutation.Field(required=True)
    delete_division = DeleteDivisionMutation.Field(required=True)

    add_period_group = AddPeriodGroupMutationPayload.Field(required=True)
    copy_period_groups = CopyPeriodGroupsMutation.Field(required=True)
    change_period_group_privileges = ChangePeriodGroupPrivilegesMutation.Field(required=True)
    delete_period_group = DeletePeriodGroupMutationPayload.Field(required=True)

    change_user_period_groups = ChangeUserPeriodGroupsMutation.Field(required=True)
    change_user_period_privileges = ChangeUserPeriodPrivileges.Field(required=True)
