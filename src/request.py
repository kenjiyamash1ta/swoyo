from typing import Optional, Dict


class HTTPRequest:
    def __init__(
        self,
        method: str = "GET",
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
    ):
        self.method = method
        self.path = path
        self.headers = headers if headers is not None else {}
        self.body = body

    def to_bytes(self) -> bytes:
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = "\r\n".join(
            f"{key}: {value}" for key, value in self.headers.items()
        )
        body = self.body if self.body else ""
        http_request = f"{request_line}{headers}\r\n\r\n{body}"
        return http_request.encode('utf-8')

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HTTPRequest":
        data = binary_data.decode('utf-8')
        lines = data.split("\r\n")
        request_line = lines[0]
        method, path, _ = request_line.split()
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ", 1)
            headers[key] = value

        body = ""
        if "\r\n\r\n" in data:
            body = data.split("\r\n\r\n", 1)[1]

        return cls(method=method, path=path, headers=headers, body=body)
