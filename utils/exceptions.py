import logging
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    handlers = {
        Http404: _handle_not_found_error,
        ObjectDoesNotExist: _handle_not_found_error,
        IntegrityError: _handle_integrity_error,
    }
    exception_type = type(exc)
    handler = handlers.get(exception_type, _handle_generic_500_error)
    response = handler(exc, context)
    return response


def _handle_not_found_error(exc, context):
    logger.error(f"Not Found Error: {str(exc)}", exc_info=True)
    return Response(
        {"detail": _("The requested resource was not found.")},
        status=status.HTTP_404_NOT_FOUND,
    )


def _handle_integrity_error(exc, context):
    logger.error(f"Integrity Error: {str(exc)}", exc_info=True)
    return Response(
        {"detail": _("A database integrity error occurred.")},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _handle_generic_500_error(exc, context):
    logger.error(f"Internal Server Error: {str(exc)}", exc_info=True)
    return Response(
        {"detail": _("An internal server error occurred.")},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
