import socket
from src.response import HTTPResponse
from src.request import HTTPRequest
from src.log import logger


def send_sms(request: HTTPRequest, host: str, port: int) -> HTTPResponse:
    try:
        with socket.create_connection((host, port)) as sock:
            sock.sendall(request.to_bytes())
            response_data = sock.recv(4096)
        logger.info("HTTP response received")
        return HTTPResponse.from_bytes(response_data)

    except Exception as e:
        logger.error(f"Error sending request: {e}")
        return HTTPResponse(
            status_code=500,
            status_message="Internal server error",
            headers={},
            body='{"error": "Internal server error"}'
        )
