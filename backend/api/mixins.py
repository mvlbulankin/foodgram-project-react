from rest_framework import status
from rest_framework.response import Response


class ErrorAlertMixin:
    @staticmethod
    def error_alert(message):
        return Response(
            {"errors": f"{message}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
