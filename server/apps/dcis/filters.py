"""Модуль описания фильтрации внешних выгрузок."""
from django.db.models import OuterRef, QuerySet, Subquery
from django.forms import MultipleChoiceField
from django_filters import MultipleChoiceFilter, filterset
from graphene import ID, List
from graphene_django.forms.converter import convert_form_field

from .models import Document, DocumentStatus


class IDMultipleChoiceField(MultipleChoiceField):
    """Поле для фильтра IDMultipleChoiceFilter."""

    def valid_value(self, value) -> bool:
        """Проверка, что пришел идентификатор."""
        if value.isdigit():
           return True
        return False


@convert_form_field.register(IDMultipleChoiceField)
def convert_form_field_to_list(field):
    """Регистрация поля IDMultipleChoiceField."""
    return List(ID, required=field.required)


class IDMultipleChoiceFilter(MultipleChoiceFilter):
    """MultipleChoiceFilter для типа ID со значением обычного id типа '1'."""

    field_class = IDMultipleChoiceField


class DocumentFilter(filterset.FilterSet):
    """Фильтр документов."""

    division_id__in = IDMultipleChoiceFilter(field_name='object_id')
    last_status__status_id__in = IDMultipleChoiceFilter(field_name='last_status__status_id')

    def filter_queryset(self, queryset: QuerySet):
        qs = queryset.annotate(
            last_status__status_id=Subquery(
                DocumentStatus.objects.filter(
                    document_id=OuterRef('pk')
                ).order_by('-created_at').values('status')[:1]
            )
        )
        return super().filter_queryset(qs)

    class Meta:
        """Мета класс настроек."""

        model = Document
        fields = []
