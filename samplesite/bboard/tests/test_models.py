from django.test import TestCase

from bboard.models import Ad, Rubric


class AdModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        rubric = Rubric.objects.create(name='Test rubric')
        Ad.objects.create(rubric=rubric, title='title', content='content', price=1.0)

    def test_rubric_label(self):
        ad = Ad.objects.get(id=1)
        field_label = ad._meta.get_field('rubric').verbose_name
        self.assertEqual(field_label, 'rubric')

    def test_title_label(self):
        ad = Ad.objects.get(id=1)
        field_label = ad._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'ZAGOLOVOK')

    def test_title_max_lenth(self):
        ad = Ad.objects.get(id=1)
        max_length = ad._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_separated(self):
        ad = Ad.objects.get(id=1)
        expected_object_name = '{} {}'.format(ad.title, ad.published)
        self.assertEqual(expected_object_name, str(ad))
