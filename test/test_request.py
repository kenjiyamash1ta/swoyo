import pytest
from src.request import Request

def test_to_bytes():
    request = Request(
        method="POST",
        path="/send_sms",
        headers={
            "Host": "localhost:4010",
            "Content-Type": "application/json",
        },
        body='{"message": "Hello, World!"}',
    )

    request_bytes = request.to_bytes()

    expected = (
        b"POST /send_sms HTTP/1.1\r\n"
        b"Host: localhost:4010\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"message": "Hello, World!"}'
    )

    assert request_bytes == expected

def test_from_bytes():
    request_bytes = (
        b"POST /send_sms HTTP/1.1\r\n"
        b"Host: localhost:4010\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"message": "Hello, World!"}'
    )

    request = Request.from_bytes(request_bytes)

    assert request.method == "POST"
    assert request.path == "/send_sms"
    assert request.headers == {
        "Host": "localhost:4010",
        "Content-Type": "application/json",
    }
    assert request.body == '{"message": "Hello, World!"}'

def test_to_bytes_and_from_bytes_roundtrip():
    original_request = Request(
        method="GET",
        path="/",
        headers={"User-Agent": "TestClient"},
        body="Test Body",
    )

    request_bytes = original_request.to_bytes()
    new_request = Request.from_bytes(request_bytes)

    assert new_request.method == original_request.method
    assert new_request.path == original_request.path
    assert new_request.headers == original_request.headers
    assert new_request.body == original_request.body

def test_from_bytes_without_body():
    request_bytes = (
        b"GET / HTTP/1.1\r\n"
        b"Host: localhost:4010\r\n"
        b"\r\n"
    )

    request = Request.from_bytes(request_bytes)

    assert request.method == "GET"
    assert request.path == "/"
    assert request.headers == {"Host": "localhost:4010"}
    assert request.body == ""

def test_from_bytes_with_empty_headers():
    request_bytes = (
        b"GET / HTTP/1.1\r\n"
        b"\r\n"
        b"Test Body"
    )

    request = Request.from_bytes(request_bytes)

    assert request.method == "GET"
    assert request.path == "/"
    assert request.headers == {}
    assert request.body == "Test Body"