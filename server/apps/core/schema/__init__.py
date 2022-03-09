import graphene
from .mutations import AuthCbiasMutation
from .types import UserType


class Mutation(graphene.ObjectType):
    """Описание пользовательских мутаций."""

    auth_cbias = AuthCbiasMutation.Field()
