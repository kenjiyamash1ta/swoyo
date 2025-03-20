import pytest
from src.response import Response

def test_to_bytes():
    # Создаём объект Response
    response = Response(
        status_code=200,
        status_message="OK",
        headers={
            "Content-Type": "application/json",
            "Content-Length": "25",
        },
        body='{"status": "success"}',
    )

    # Преобразуем в байты
    response_bytes = response.to_bytes()

    # Ожидаемый результат
    expected = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 25\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )

    # Проверяем, что результат совпадает с ожидаемым
    assert response_bytes == expected

def test_from_bytes():
    # Пример HTTP-ответа в байтах
    response_bytes = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 25\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )

    # Преобразуем байты в объект Response
    response = Response.from_bytes(response_bytes)

    # Проверяем, что объект Response создан корректно
    assert response.status_code == 200
    assert response.status_message == "OK"
    assert response.headers == {
        "Content-Type": "application/json",
        "Content-Length": "25",
    }
    assert response.body == '{"status": "success"}'

def test_to_bytes_and_from_bytes_roundtrip():
    # Создаём объект Response
    original_response = Response(
        status_code=404,
        status_message="Not Found",
        headers={"X-Custom-Header": "Value"},
        body="Not Found",
    )

    # Преобразуем в байты и обратно
    response_bytes = original_response.to_bytes()
    new_response = Response.from_bytes(response_bytes)

    # Проверяем, что объекты идентичны
    assert new_response.status_code == original_response.status_code
    assert new_response.status_message == original_response.status_message
    assert new_response.headers == original_response.headers
    assert new_response.body == original_response.body

def test_from_bytes_without_body():
    # Пример HTTP-ответа без тела
    response_bytes = (
        b"HTTP/1.1 204 No Content\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
    )

    # Преобразуем байты в объект Response
    response = Response.from_bytes(response_bytes)

    # Проверяем, что объект Response создан корректно
    assert response.status_code == 204
    assert response.status_message == "No Content"
    assert response.headers == {"Content-Type": "text/plain"}
    assert response.body == ""

def test_from_bytes_with_empty_headers():
    # Пример HTTP-ответа без заголовков
    response_bytes = (
        b"HTTP/1.1 200 OK\r\n"
        b"\r\n"
        b"Hello, World!"
    )

    # Преобразуем байты в объект Response
    response = Response.from_bytes(response_bytes)

    # Проверяем, что объект Response создан корректно
    assert response.status_code == 200
    assert response.status_message == "OK"
    assert response.headers == {}
    assert response.body == "Hello, World!"