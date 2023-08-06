import json
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status
import traceback
from django.conf import settings

import inflect
p = inflect.engine()
def pluralize(word):
    return p.plural(word.lower())

def DBExceptionHandler(ex, context):
    # Ref: https://stackoverflow.com/questions/33450390/django-rest-framework-database-error-exception-handling
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(ex, context)
    # if there is an IntegrityError and the error response hasn't already been generated
    request = context["request"]
    errorData = {
        "status": "ERROR",
        "path": request.path,
        "method": request.method,
        "content_type": request.content_type,
        "query_params": request.query_params,
        "body": request.data,
        "error": ex.__str__()
    }
    errorJson = json.dumps(errorData, indent=4)
    print(errorJson)

    # print error to console
    if settings.DEBUG:
        print("[[ STACKTRACE ]]")
        traceback.print_exc()

    if isinstance(ex, IntegrityError) and not response:
        response = Response(
            {
                'detail': ex.__str__(),
                'code': "bad_request"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(ex, TypeError) and not response:
        response = Response(
            {
                'detail': ex.__str__(),
                'code': "system_error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if isinstance(ex, ValidationError):
        response = Response(
            {
                'detail': ex.args[0],
                'code': "bad_request"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(ex, CoreValidationError):
        response = Response(
            {
                'detail': ex.args[0],
                'code': "bad_request"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return response
