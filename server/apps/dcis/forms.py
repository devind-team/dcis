

from django import forms
from apps.dcis.models import Attribute


class AddAttributeForm(forms.ModelForm):
    """Форма для создания атрибута."""

    class Meta:

        model = Attribute
        fields = (
            'name',
            'placeholder',
            'key',
            'kind',
            'default',
            'mutable',
            'position',
            'period',
            'parent',
        )

    default = forms.CharField(max_length=512, required=False)
    position = forms.IntegerField(default=0, required=False)
    parent = forms.ModelChoiceField(queryset=Attribute.objects.all(), required=False)


class ChangeAttributeForm(AddAttributeForm):
    """Форма для изменения атрибута."""

    class Meta(AddAttributeForm.Meta):
        fields = (
            'id',
            'name',
            'placeholder',
            'key',
            'kind',
            'default',
            'mutable',
        )
