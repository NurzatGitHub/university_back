from datetime import datetime

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import Token

from users.models import User
from .models import Course, Group, Lesson, LessonAttendance, Reference


class CreateCourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password', is_teacher=True)
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        url = reverse('create_course')
        data = {
            'course_name': 'Test Course',
            'teacher': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_without_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('create_course')
        data = {
            'course_name': 'Test Course',
            'teacher': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetMyLessonsWithAttendanceTypeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(course_name='Somecourse', teacher=self.user)
        self.group = Group.objects.create(group_name='Somegroup', course=self.course)
        self.lesson = Lesson.objects.create(group=self.group, lesson_date=timezone.now())

    def test_get_lessons_with_attendance(self):
        url = reverse('get_my_lessons_with_attendance_type', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lessons_with_attendance_without_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('get_my_lessons_with_attendance_type', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SendReferenceToLessonTests(APITestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher_user', password='teacher_password', is_teacher=True)
        self.student_user = User.objects.create_user(username='student_user', password='student_password')
        self.client.force_authenticate(user=self.student_user)

        self.course = Course.objects.create(course_name='Somecourse', teacher=self.teacher_user)
        self.group = Group.objects.create(group_name='Somegroup', course=self.course)
        self.lesson = Lesson.objects.create(group=self.group, lesson_date='2024-04-18-12-00')

        data = {
            'username': "student_user",
            'password': "student_password",
        }
        url = reverse('token_obtain_pair')

        respo = self.client.post(url, data, format='json')
        self.token = respo.data['access']

    def test_send_reference_to_lesson(self):
        url = reverse('send_reference_to_lesson', kwargs={'lesson_id': self.lesson.id})
        responseIM = requests.get('https://formula-med.com/upload/iblock/d79/d79427851472ba3e0cc612fdfd0a2714.jpg')
        image_content = responseIM.content
        image_file = SimpleUploadedFile("image.jpg", image_content)
        data = {
            'file': image_file,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
