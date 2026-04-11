import uuid
import threading

_thread_locals = threading.local()


def get_request_id():
    """Get the request ID for the current thread."""

    return getattr(_thread_locals, "request_id", "-")


class RequestIDMiddleware:
    """Middleware to generate a unique request ID for each incoming request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request_id = str(uuid.uuid4())[:8]
        response = self.get_response(request)
        response["X-Request-ID"] = _thread_locals.request_id
        return response
