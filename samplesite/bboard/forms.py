from django import forms
from django.forms.widgets import Select
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from bboard.models import Ad, Rubric


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['title', 'content', 'price', 'rubric']
        labels = {'title': 'NAZVANIE',}
        help_text = {'rubric': 'Dont forget to specify rubric'}
        field_classes = {'price': forms.DecimalField, }


    def clean_title(self):
        val = self.cleaned_data.get('title')
        if val == 'Previous year snow':
            raise ValidationError('message')
        return val

    def clean(self):
        super(AdForm, self).clean()
        errors = dict()

        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Set content for yor item')

        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Price must be positive')

        if errors:
            raise ValidationError(errors)

