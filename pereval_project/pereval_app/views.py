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