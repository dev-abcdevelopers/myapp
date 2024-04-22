from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APIClient, force_authenticate

class APIKeyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('generate_api_key')
        self.client.force_authenticate(user=self.user) 

    def test_generate_api_key(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('api_key', response.data)

    def test_prevent_multiple_keys(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        second_response = self.client.post(self.url)
        self.assertEqual(second_response.status_code, 400)