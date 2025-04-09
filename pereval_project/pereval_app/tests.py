from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Coords, Level, PerevalAdded


class PerevalApiTests(APITestCase):
    def setUp(self):
        # Создаём тестовые данные
        self.user_data = {
            "email": "test@mail.ru",
            "fam": "Тестов",
            "name": "Тест",
            "otc": "Тестович",
            "phone": "+7 999 999 99 99"
        }

        self.coords_data = {
            "latitude": 55.75,
            "longitude": 37.61,
            "height": 300
        }

        self.level_data = {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        }

        self.images_data = [
            {"data": "<image1>", "title": "Фото 1"},
            {"data": "<image2>", "title": "Фото 2"}
        ]

        self.pereval_data = {
            "beauty_title": "пер. ",
            "title": "Тестовый перевал",
            "other_titles": "Альтернативный",
            "connect": "",
            "add_time": "2024-04-01T10:00:00",
            "user": self.user_data,
            "coords": self.coords_data,
            "level": self.level_data,
            "images": self.images_data
        }

    def test_create_and_get_pereval(self):
        # Отправляем POST запрос на создание перевала
        url_post = reverse("submit_data")
        response_post = self.client.post(url_post, self.pereval_data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["status"], 200)

        pereval_id = response_post.data["id"]

        # Получаем созданный перевал по ID
        url_get = reverse("submit_data_detail", args=[pereval_id])
        response_get = self.client.get(url_get)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data["title"], self.pereval_data["title"])
        self.assertEqual(response_get.data["user"]["email"], self.user_data["email"])

    def test_patch_pereval_allowed_fields(self):
        # Сначала создаём перевал
        response_post = self.client.post('/api/submitData/', self.pereval_data, format='json')
        pereval_id = response_post.data['id']

        # Отправляем PATCH с разрешёнными полями (например, меняем название)
        update_data = {
            "title": "Обновлённый перевал",
            "beauty_title": "пер. Обновлённый",
            "coords": {
                "latitude": 50.0000,
                "longitude": 30.0000,
                "height": 1500
            },
            "level": {
                "winter": "",
                "summer": "1Б",
                "autumn": "1Б",
                "spring": ""
            }
        }

        response_patch = self.client.patch(f'/api/submitData/{pereval_id}/edit/', update_data, format='json')

        self.assertEqual(response_patch.status_code, 200)
        self.assertEqual(response_patch.data["state"], 1)
        self.assertEqual(response_patch.data["message"], "Успешно обновлено")

        # Проверим, что данные действительно обновлены
        response_get = self.client.get(f'/api/submitData/{pereval_id}/')
        self.assertEqual(response_get.data["title"], "Обновлённый перевал")
        self.assertEqual(response_get.data["level"]["summer"], "1Б")
        self.assertEqual(response_get.data["coords"]["height"], 1500)
