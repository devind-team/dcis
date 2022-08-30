from datetime import date
from typing import Any

import graphene
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.models import Period, PeriodGroup, Project
from apps.dcis.schema.types import DivisionModelType, PeriodGroupType, PeriodType, PrivilegeType
from apps.dcis.services.period_services import (
    add_divisions_period,
    add_period_group,
    add_divisions_from_file,
    change_period_group_privileges,
    change_settings_period,
    change_user_period_groups,
    change_user_period_privileges,
    copy_period_groups,
    create_period,
    delete_divisions_period,
    delete_period,
    delete_period_groups,
)


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='xlsx файл с проектом')
        multiple = graphene.Boolean(required=True, description='Множественный тип сбора')
        readonly_fill_color = graphene.Boolean(required=True, description='Запретить редактирование ячеек с заливкой')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        name: str,
        project_id: str,
        file: InMemoryUploadedFile,
        multiple: bool,
        readonly_fill_color: bool
    ):
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        return AddPeriodMutation(
            period=create_period(
                name=name,
                user=info.context.user,
                project=project,
                multiple=multiple,
                file=file,
                readonly_fill_color=readonly_fill_color
            )
        )


class ChangePeriodMutation(BaseMutation):
    """Мутация на изменение настроек периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор текущего периода')
        name = graphene.String(required=True, description='Название периода')
        status = graphene.String(required=True, description='Статус проекта')
        multiple = graphene.Boolean(required=True, description='Множественное заполнение')
        privately = graphene.Boolean(required=True, description='Приватность полей')
        start = graphene.Date(required=False, description='Дата начала')
        expiration = graphene.Date(required=False, description='Дата окончания')

    period = graphene.Field(PeriodType, description='Измененный период')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(
        root: Any,
        info: ResolveInfo,
        period_id: str,
        name: str,
        status: str,
        multiple: bool,
        privately: bool,
        start: date,
        expiration: date
    ):
        period = get_object_or_404(Period, pk=period_id)
        return ChangePeriodMutation(
            period=change_settings_period(
                user=info.context.user,
                period=period,
                name=name,
                status=status,
                multiple=multiple,
                privately=privately,
                start=start,
                expiration=expiration
            )
        )


class DeletePeriodMutation(BaseMutation):
    """Мутация на удаление периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного периода')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str):
        period = get_object_or_404(Period, pk=period_id)
        delete_period(user=info.context.user, period=period)
        return DeletePeriodMutation(delete_id=period_id)


class AddDivisionsMutation(BaseMutation):
    """Мутация на добавление дивизионов в период."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы дивизионов')

    divisions = graphene.List(DivisionModelType, required=True, description='Новые дивизионы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_ids: list[str]):
        return AddDivisionsMutation(
            divisions=add_divisions_period(
                user=info.context.user,
                period_id=period_id,
                division_ids=division_ids
            )
        )


class AddDivisionsFromFileMutation(BaseMutation):
    """Мутация для добавления дивизионов из файла."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        file = Upload(requires=True, description='Файл в формате xlsx, csv')

    divisions = graphene.List(DivisionModelType, required=True, description='Новые дивизионы')
    missing_divisions = graphene.List(graphene.Int, required=True, description='Не найденные дивизионы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, file: InMemoryUploadedFile):
        """Мутация для загрузки дивизионов из файла."""
        divisions, missing_divisions, errors = add_divisions_from_file(
            info.context.user,
            period_id,
            file
        )
        return AddDivisionsFromFileMutation(
            success=not errors,
            divisions=divisions,
            missing_divisions=missing_divisions,
            errors=errors
        )


class DeleteDivisionMutation(BaseMutation):
    """Мутация на удаление дивизиона из периода."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор периода')
        division_id = graphene.ID(required=True, description='Идентификатор дивизиона')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленного дивизиона')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_id: str):
        delete_divisions_period(
            user=info.context.user,
            period_id=period_id,
            division_id=division_id
        )
        return DeleteDivisionMutation(delete_id=division_id)


class AddPeriodGroupMutation(BaseMutation):
    """Мутация на добавление группы в период."""

    class Input:
        name = graphene.String(required=True, description='Название группы периода')
        period_id = graphene.ID(required=True, description='Идентификатор периода')

    period_group = graphene.Field(PeriodGroupType, description='Добавленная группа периода')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str, period_id: str | int):
        return AddPeriodGroupMutation(
            period_group=add_period_group(
                user=info.context.user,
                name=name,
                period_id=period_id
            )
        )


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
        return CopyPeriodGroupsMutation(
            period_groups=copy_period_groups(
                user=info.context.user,
                period_id=period_id,
                period_group_ids=period_group_ids,
                selected_period_id=selected_period_id
            )
        )


class ChangePeriodGroupPrivilegesMutation(BaseMutation):
    """Мутация на изменение привилегий группы."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')
        privileges_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы привилегий')

    privileges = graphene.List(PrivilegeType, required=True, description='Привилегии группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: int, privileges_ids: list[str]):
        return ChangePeriodGroupPrivilegesMutation(
            privileges=change_period_group_privileges(
                user=info.context.user,
                period_group_id=period_group_id,
                privileges_ids=privileges_ids
            )
        )


class DeletePeriodGroupMutation(BaseMutation):
    """Мутация на удаление группы периода."""

    class Input:
        period_group_id = graphene.ID(required=True, description='Идентификатор группы периода')

    delete_id = graphene.ID(required=True, description='Идентификатор удаленной группы периода')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: str):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        delete_period_groups(user=info.context.user, period_group=period_group)
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
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_group_ids: list[PeriodGroup]):
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        user.periodgroup_set.set(change_user_period_groups(user=info.context.user, period_group_ids=period_group_ids))
        return ChangeUserPeriodGroupsMutation(
            user=user,
            period_groups=change_user_period_groups(user=info.context.user, period_group_ids=period_group_ids)
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
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, user_id: str, period_id: str, privileges_ids: list[str]):
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        return ChangeUserPeriodPrivilegesMutation(
            user=user,
            privileges=change_user_period_privileges(
                user=info.context.user,
                user_id=user.id,
                period_id=period_id,
                privileges_ids=privileges_ids
            )
        )


class PeriodMutations(graphene.ObjectType):
    """Список мутация периода."""

    add_period = AddPeriodMutation.Field(required=True)
    change_period = ChangePeriodMutation.Field(required=True)
    delete_period = DeletePeriodMutation.Field(required=True)

    add_divisions = AddDivisionsMutation.Field(required=True)
    add_divisions_from_file = AddDivisionsFromFileMutation.Field(required=True)
    delete_division = DeleteDivisionMutation.Field(required=True)

    add_period_group = AddPeriodGroupMutation.Field(required=True)
    copy_period_groups = CopyPeriodGroupsMutation.Field(required=True)
    change_period_group_privileges = ChangePeriodGroupPrivilegesMutation.Field(required=True)
    delete_period_group = DeletePeriodGroupMutation.Field(required=True)

    change_user_period_groups = ChangeUserPeriodGroupsMutation.Field(required=True)
    change_user_period_privileges = ChangeUserPeriodPrivilegesMutation.Field(required=True)
