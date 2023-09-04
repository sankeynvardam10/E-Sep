import json
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class ResignationDetailedViewTestCases(TestCase):
    
    def setUp(self):
        # adding records to db
        ...

    def test_resignation_details_get_method(self):
        url = reverse('resignation')
        response = self.client.get(url)
        if response:
            self.assertEqual(response.status_code, 201, "--- test_resignation_details_get_method ===> response.status_code is not 200")
        # response = response.content.decode('utf-8')
        # response = json.loads(response)
        # self.assertEqual()