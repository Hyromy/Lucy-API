from django.http import HttpResponse
from utils.logger import RequestIDMiddleware, get_request_id, _thread_locals


class TestLoggerUtils:
    def test_get_request_id_default(self):
        """Test that get_request_id returns '-' by default when no ID is set."""

        if hasattr(_thread_locals, "request_id"):
            del _thread_locals.request_id

        assert get_request_id() == "-"

    def test_middleware_generates_id(self):
        """Test that the middleware generates a request ID and adds it to the response."""

        def get_response(request):
            return HttpResponse("OK")

        middleware = RequestIDMiddleware(get_response)
        request = type("MockRequest", (), {})()

        response = middleware(request)

        current_id = get_request_id()
        assert current_id != "-"
        assert len(current_id) == 8

        assert response["X-Request-ID"] == current_id

    def test_middleware_cleans_up_or_overwrites(self):
        """Test that different calls generate different IDs."""

        def get_response(request):
            return HttpResponse("OK")

        middleware = RequestIDMiddleware(get_response)
        request = type("MockRequest", (), {})()

        response1 = middleware(request)
        id1 = response1["X-Request-ID"]

        response2 = middleware(request)
        id2 = response2["X-Request-ID"]

        assert id1 != id2
        assert get_request_id() == id2
