from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PerevalAdded
from .serializers import PerevalAddedSerializer


class SubmitDataView(APIView):
    def post(self, request):
        try:
            serializer = PerevalAddedSerializer(data=request.data)
            if serializer.is_valid():
                pereval = serializer.save()
                return Response(
                    {
                        "status": 200,
                        "message": None,
                        "id": pereval.id
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "status": 400,
                        "message": "Ошибка валидации данных",
                        "errors": serializer.errors,
                        "id": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "status": 500,
                    "message": f"Ошибка сервера: {str(e)}",
                    "id": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubmitDataDetailView(APIView):
    def get(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
            serializer = PerevalAddedSerializer(pereval)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PerevalAdded.DoesNotExist:
            return Response(
                {"message": "Запись не найдена", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )


class SubmitDataUpdateView(APIView):
    def patch(self, request, id):
        try:
            # Проверка на пустой JSON
            if not request.data:
                return Response(
                    {"state": 0, "message": "Пустой запрос: отсутствуют данные для обновления"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Получаем запись перевала по ID
            pereval = PerevalAdded.objects.get(id=id)

            # Проверяем статус записи
            if pereval.status != 'new':
                return Response(
                    {"state": 0, "message": "Редактирование запрещено: статус не 'new'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверяем наличие запрещенных полей
            forbidden_fields = ["email", "fam", "name", "otc", "phone"]
            if "user" in request.data:
                user_data = request.data.get("user")
                # Если хотя бы одно запрещенное поле присутствует, возвращаем ошибку
                if any(field in user_data for field in forbidden_fields):
                    return Response(
                        {"state": 0, "message": "Нельзя редактировать ФИО, адрес почты и номер телефона"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Обновляем данные
            serializer = PerevalAddedSerializer(pereval, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"state": 1, "message": "Успешно обновлено"}, status=status.HTTP_200_OK)

            return Response({"state": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except PerevalAdded.DoesNotExist:
            return Response(
                {"state": 0, "message": "Запись не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"state": 0, "message": f"Ошибка: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

