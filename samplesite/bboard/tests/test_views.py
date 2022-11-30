from django.test import TestCase
from django.urls import reverse

from bboard.models import Ad, Rubric


class AdListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_ads = 13
        rubric = Rubric.objects.create(name='Test rubric')
        for elem in range(number_of_ads):
            Ad.objects.create(rubric=rubric, title='title {}'.format(elem), content='content', price=1.0)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/bboard/')
        self.assertEqual(resp.status_code, 200)

    def test_lists_all_ads(self):
        resp = self.client.get('/bboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['ads']) == 13)
