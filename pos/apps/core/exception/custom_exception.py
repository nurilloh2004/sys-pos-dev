"""
Handled exceptions raised CustomValidationError.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomValidationError(APIException):
    status_code = status.HTTP_200_OK
    # default_detail = _('Invalid input.')
    default_detail = _('validation error.')
    default_message = _('Not found')
    default_code = 3  # POSResponse.CODE_3
    debug: tuple = None

    def __init__(self, debug: str = None):

        response = {'success': False, 'code': self.default_code, 'message': f"{self.default_detail}"}
        if debug is not None:
            response['debug'] = [debug]
        self.detail = response
