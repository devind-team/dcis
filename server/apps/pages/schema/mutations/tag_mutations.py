import graphene
from graphql import ResolveInfo

from apps.pages.models import Tag
from apps.pages.validators import TagValidator
from devind_helpers.schema.types import ErrorFieldType
from devind_helpers.decorators import permission_classes
from devind_helpers.permissions import IsAuthenticated
from devind_helpers.schema.mutations import BaseMutation
from ..types import TagType
from ...permissions import AddTag


class AddTagMutation(BaseMutation):
    """Добавление тега"""
    class Input:
        name = graphene.String(required=True, verbose_name='Название')

    tag = graphene.Field(TagType, description='Добавленный тег')

    @staticmethod
    @permission_classes([IsAuthenticated, AddTag])
    def mutate_and_get_payload(root, info: ResolveInfo, *args, **kwargs):
        data = Tag.resolve_global({**kwargs, 'user_id': info.context.user.pk})
        validator: TagValidator = TagValidator(data)
        if validator.validate():
            tag: Tag = Tag.objects.create(**data)
            return AddTagMutation(tag=tag)
        return AddTagMutation(success=False, errors=ErrorFieldType.from_validator(validator.get_message()))


class TagMutations(graphene.ObjectType):
    add_tag = AddTagMutation.Field(required=True)
