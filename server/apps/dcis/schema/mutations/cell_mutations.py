"""Модуль содержит мутации, относящиеся к ячейкам."""

import graphene
from devind_dictionaries.models import BudgetClassification
from devind_dictionaries.schema.types import BudgetClassificationType
from graphene_django_cud.mutations import DjangoCreateMutation


class AddBudgetClassificationMutationPayload(DjangoCreateMutation):
    """Мутация для добавления КБК в словарь."""

    class Meta:
        model = BudgetClassification
        login_required = True
        required_fields = ('code', 'name',)
        permissions = ('devind_dictionaries.add_budgetclassification',) # noqa

    budget_classification = graphene.Field(BudgetClassificationType, description='Добавленная КБК')


class CellMutations(graphene.ObjectType):
    """Мутации, связанные с ячейками."""

    add_budget_classification = AddBudgetClassificationMutationPayload.Field(
        required=True,
        description='Добавление нового КБК'
    )
