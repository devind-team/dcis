from typing import Any

import graphene
from devind_core.models import File
from devind_dictionaries.models import Department
from devind_helpers.decorators import permission_classes
from devind_helpers.orm_utils import get_object_or_404
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoDeleteMutation, DjangoUpdateMutation
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_relay import from_global_id

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.helpers import DjangoCudBaseMutation
from apps.dcis.models import Division
from apps.dcis.models import Project, Period, PeriodGroup, PeriodPrivilege
from apps.dcis.permissions import AddPeriod
from apps.dcis.schema.types import PeriodGroupType, ProjectType, PeriodType, DivisionType
from apps.dcis.services.excel_extractor import ExcelExtractor
from apps.dcis.validators import ProjectValidator


class AddProjectMutationPayload(DjangoCudBaseMutation, DjangoCreateMutation):
    """Мутация для добавления проекта."""

    class Meta:
        model = Project
        login_required = True
        field_types = {
            'content_type': graphene.String(required=True)
        }
        permissions = ('dcis.add_project',)

    project = graphene.Field(ProjectType, description='Добавленный проект')

    @classmethod
    def validate(cls, root: Any, info: ResolveInfo, input, *args, **kwargs):
        validator: ProjectValidator = ProjectValidator(input)
        if validator.validate():
            super().validate(root, info, input)
        else:
            raise ValueError(validator.validate_message_plain)

    @classmethod
    def handle_content_type(cls, value: str, field: str, info: ResolveInfo, *args, **kwargs):
        return ContentType.objects.get_for_model(Project.DIVISION_KIND.get(value, Department))


class ChangeProjectMutationPayload(DjangoCudBaseMutation, DjangoUpdateMutation):
    """Мутация изменения настроек проекта."""

    class Meta:
        model = Project
        login_required = True
        exclude_fields = ('content_type', 'object_id',)
        permissions = ('dcis.change_project',)

    project = graphene.Field(ProjectType, description='Измененный проект')


class DeleteProjectMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление проекта."""

    class Meta:
        model = Project
        login_required = True
        permissions = ('dcis.delete_project',)


class AddPeriodMutation(BaseMutation):
    """Мутация для создания периода."""

    class Input:
        name = graphene.String(required=True, description='Название периода')
        project_id = graphene.ID(required=True, description='Идентификатор проекта')
        file = Upload(required=True, description='Xlsx файл с проектом')

    period = graphene.Field(PeriodType, description='Добавленный период')

    @staticmethod
    @permission_classes((IsAuthenticated, AddPeriod,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, name: str, project_id: str, file: InMemoryUploadedFile):
        project = get_object_or_404(Project, pk=from_global_id(project_id)[1])
        period: Period = Period.objects.create(
            name=name,
            user=info.context.user,
            project=project
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
        permissions = ('dcis.change_period',)

    period = graphene.Field(PeriodType, description='Измененный период')


class DeletePeriodMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление периода."""

    class Meta:
        model = Period
        login_required = True
        permissions = ('dcis.delete_period',)


class ChangeDivisionsMutation(BaseMutation):
    """Мутация на изменение дивизионов."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор текущего периода')
        division_ids = graphene.List(graphene.NonNull(graphene.ID), description='Идентификаторы дивизионов')

    divisions = graphene.List(DivisionType, required=True, description='Новые дивизионы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, division_ids: list[str]):
        period = get_object_or_404(Period, pk=period_id)
        for division_id in division_ids:
            Division.objects.create(period=period, object_id=division_id)
        return ChangeDivisionsMutation(divisions=period.division_set.all())


class DeleteDivisionsMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление объекта из периода."""

    class Meta:
        model = Division
        login_required = True
        permissions = ('dcis.delete_division',)


class AddPeriodGroupMutationPayload(DjangoCudBaseMutation, DjangoCreateMutation):
    """Мутация на добавление группы периода."""

    class Meta:
        model = PeriodGroup
        login_required = True
        permissions = ('dcis.add_periodgroup',)
        exclude_fields = ('users', 'privileges',)


class CopyPeriodGroupMutation(BaseMutation):
    """Мутация на перенос группы с пользователями из другого сбора."""

    class Input:
        period_id = graphene.ID(required=True, description='Идентификатор текущего периода')
        selected_period_id = graphene.ID(required=True, description='Идентификатор выбранного периода')
        period_groups_ids = graphene.List(graphene.NonNull(graphene.ID), description='Выбранные группы')

    period_groups = graphene.List(PeriodGroupType, required=True, description='Группы сбора')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_id: str, selected_period_id: str, period_groups_ids: list[str]):
        selected_period = get_object_or_404(Period, pk=selected_period_id)
        period = get_object_or_404(Period, pk=period_id)
        period_groups: list[PeriodGroup] = []
        for period_group_id in period_groups_ids:
            period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
            period_groups.append(period_group)
            new_group = PeriodGroup.objects.create(name=period_group.name, period=period)
            new_group.users.set(period_group.users.all())
            new_group.privileges.set(period_group.privileges.all())
            for user in period_group.users.all():
                for period_privilege in user.periodprivilege_set.filter(period=selected_period).all():
                    PeriodPrivilege.objects.create(period=period, user=user, privilege=period_privilege.privilege)
        return CopyPeriodGroupMutation(period_groups=period_groups)


class ChangePeriodGroupUsersMutation(BaseMutation):
    """Мутация на добавление пользователей в группу."""

    class Input:
        period_group_id = graphene.Int(required=True, description='Идентификатор группы периода')
        users_ids = graphene.List(graphene.NonNull(graphene.ID), description='Пользователи')

    users = graphene.List(UserType, required=True, description='Измененная пользователи группы')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: str, users_ids: list[str]):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        users: list[User] = list(period_group.users.all())
        for user_id in users_ids:
            user = get_object_or_404(User, pk=from_global_id(user_id)[1])
            users.append(user)
        period_group.users.set(users)
        return ChangePeriodGroupUsersMutation(users=users)


class DeletePeriodGroupMutationPayload(DjangoCudBaseMutation, DjangoDeleteMutation):
    """Мутация на удаление группы сбора."""

    class Meta:
        model = PeriodGroup
        login_required = True
        permissions = ('dcis.delete_periodgroup',)


class DeleteUserFromPeriodGroupMutation(BaseMutation):
    """Мутация на удаление пользователя из группы."""

    class Input:
        period_group_id = graphene.Int(required=True, description='Идентификатор группы периода')
        user_id = graphene.ID(required=True, description='Идентификатор пользователя')

    id = graphene.ID(required=True, description='Идентификатор удаленного пользователя')

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo, period_group_id: str, user_id: str):
        period_group = get_object_or_404(PeriodGroup, pk=period_group_id)
        user = get_object_or_404(User, pk=from_global_id(user_id)[1])
        period_group.users.remove(user)
        PeriodPrivilege.objects.filter(user=user).all().delete()
        return DeleteUserFromPeriodGroupMutation(id=user_id)


class ProjectMutations(graphene.ObjectType):
    """Список мутация проекта."""

    add_project = AddProjectMutationPayload.Field(required=True)
    change_project = ChangeProjectMutationPayload.Field(required=True)
    delete_project = DeleteProjectMutationPayload.Field(required=True)
    add_period = AddPeriodMutation.Field(required=True)
    change_period = ChangePeriodMutationPayload.Field(required=True)
    delete_period = DeletePeriodMutationPayload.Field(required=True)
    change_divisions = ChangeDivisionsMutation.Field(required=True)
    delete_division = DeleteDivisionsMutationPayload.Field(required=True)

    add_period_group = AddPeriodGroupMutationPayload.Field(required=True)
    copy_period_groups = CopyPeriodGroupMutation.Field(required=True)
    delete_period_group = DeletePeriodGroupMutationPayload.Field(required=True)
    change_period_group_users = ChangePeriodGroupUsersMutation.Field(required=True)
    delete_user_from_period_group = DeleteUserFromPeriodGroupMutation.Field(required=True)
