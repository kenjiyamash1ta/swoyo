from typing import Dict, Optional

class HTTPResponse:
    def __init__(
        self,
        status_code: int = 200,
        status_message: str = "OK",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
    ):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers if headers is not None else {}
        self.body = body

    def to_bytes(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"
        headers = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())
        body = self.body if self.body else ""
        http_response = f"{status_line}{headers}\r\n\r\n{body}"
        return http_response.encode('utf-8')

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HTTPResponse":
        data = binary_data.decode('utf-8')
        lines = data.split("\r\n")

        status_line = lines[0]
        _, status_code, status_message = status_line.split(" ", 2)
        status_code = int(status_code)

        headers = {}
        body = ""
        is_body = False
        for line in lines[1:]:
            if not line.strip():
                is_body = True
                continue
            if is_body:
                body += line
            else:
                if ": " in line:  
                    key, value = line.split(": ", 1)
                    headers[key] = value

        return cls(status_code=status_code, status_message=status_message, headers=headers, body=body)