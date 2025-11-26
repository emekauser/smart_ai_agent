
from rest_framework import status
from rest_framework.test import APITestCase


class DocumentViewTest(APITestCase):
    def setUp(self):
        pass

    def test_get_document_list(self):
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 0)
