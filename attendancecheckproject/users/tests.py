from .models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ChangeUserInfoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password',
                                             first_name='Old', last_name='User')

    def test_change_user_info(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('change-user-info')
        new_first_name = 'New'
        new_last_name = 'User'
        data = {'first_name': new_first_name, 'last_name': new_last_name}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, new_first_name)
        self.assertEqual(self.user.last_name, new_last_name)


class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='old_password')

    def test_change_password(self):
        url = reverse('change-password')
        new_password = 'new_password'
        data = {'username': 'test_user', 'new_password': new_password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(username='test_user').check_password(new_password))
