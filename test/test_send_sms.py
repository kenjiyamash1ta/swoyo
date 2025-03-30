from unittest.mock import patch, MagicMock
from src.request import HTTPRequest
from src.send_sms import send_sms


def test_send_sms_success():
    """
    Проверяем успешную отправку запроса и получение ответа.
    """
    # Мок HTTP-запроса
    mock_request = HTTPRequest(
        method="POST",
        path="/send_sms",
        headers={"Content-Type": "application/json"},
        body='{"message": "Hello, World!"}',
    )

    # Мок HTTP-ответа
    mock_response_data = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )

    # Мок сокета
    with patch("socket.create_connection") as mock_create_connection:
        mock_sock = MagicMock()
        mock_sock.recv.return_value = mock_response_data
        mock_create_connection.return_value.__enter__.return_value = mock_sock

        # Вызываем функцию send_sms
        response = send_sms(mock_request, "localhost", 8080)

        # Проверяем, что ответ корректен
        assert response.status_code == 200
        assert response.status_message == "OK"
        assert response.body == '{"status": "success"}'


def test_send_sms_error():
    """
    Проверяем обработку ошибки при отправке запроса.
    """
    # Мок HTTP-запроса
    mock_request = HTTPRequest(
        method="POST",
        path="/send_sms",
        headers={"Content-Type": "application/json"},
        body='{"message": "Hello, World!"}',
    )

    # Мок сокета, который вызывает исключение
    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.side_effect = Exception("Connection error")

        # Вызываем функцию send_sms
        response = send_sms(mock_request, "localhost", 8080)

        # Проверяем, что возвращён ответ с ошибкой
        assert response.status_code == 500
        assert response.status_message == "Internal server error"
        assert response.body == '{"error": "Internal server error"}'
