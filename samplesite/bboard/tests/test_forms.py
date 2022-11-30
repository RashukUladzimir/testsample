from django.test import TestCase

from bboard.models import Ad, Rubric
from bboard.forms import AdForm


class AdFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rubric = Rubric.objects.create(name='Test rubric')

    def test_title_field_label(self):
        form = AdForm()
        self.assertTrue(form.fields['title'].label == 'NAZVANIE')

    def test_ad_form_valid(self):
        form_data = {
            'title': 'title',
            'content': 'content',
            'price': 1.0,
            'rubric': self.rubric,
        }

        form = AdForm(form_data)
        self.assertTrue(form.is_valid())

    def test_ad_form_invalid(self):
        form_data = {
            'title': 'Previous year snow',
            'content': 'content',
            'price': 1.0,
            'rubric': self.rubric,
        }
        form = AdForm(form_data)
        self.assertFalse(form.is_valid())