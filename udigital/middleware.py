import json
import logging
import socket
import time

from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import underscoreize

from udigital import settings

request_logger = logging.getLogger('main')


class CamelCaseMiddleWare:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.USE_TEST_MIDDLEWARE:
            return self.get_response(request)

        request.GET = underscoreize(
            request.GET,
            **api_settings.JSON_UNDERSCOREIZE
        )

        start_time = time.time()
        log_data = {
            "remoteAddress": request.META["REMOTE_ADDR"],
            "serverHostname": socket.gethostname(),
            "requestMethod": request.method,
            "requestPath": request.get_full_path(),
        }

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
            log_data["requestBody"] = req_body

        response = self.get_response(request)

        # add runtime to our log_data
        if 'content' in response and response.content is not None:
            log_data["responseBody"] = response.content
        log_data["runTime"] = time.time() - start_time

        request_logger.info(msg=log_data)

        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
