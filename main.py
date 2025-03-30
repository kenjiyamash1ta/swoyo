from src.config import read_cfg
from src.parser import parse
from src.log import logger
from src.request import HTTPRequest
from src.send_sms import send_sms

import base64
import json


def main():
    try:
        # Чтение конфигурации
        cfg = read_cfg()
        sender, recipient, message = parse()

        logger.info(
            (
                f"Start sending: sender={sender}, recipient={recipient}, "
                f"message={message}"
            )
        )

        # Формирование заголовка авторизации
        auth = base64.b64encode(
            f"{cfg['username']}:{cfg['password']}".encode()
            ).decode()
        content = json.dumps({
            "sender": sender,
            "recipient": recipient,
            "message": message
        })

        # Создание HTTP-запроса
        request = HTTPRequest(
            method="POST",
            path="/send_sms",
            headers={
                "Host": cfg['host'],
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth}",
                "Content-Length": str(len(content))
            },
            body=content
        )

        # Отправка запроса
        try:
            logger.debug(f"Request: {request.to_bytes().decode('utf-8')}")
            response = send_sms(request, cfg['host'], cfg['port'])
            print(response.status_code, response.body)
            logger.info(
                f"Server response: {response.status_code} "
                f"{response.status_message}\n{response.body}"
            )
        except Exception as e:
            logger.error(f"HTTPRequest failed: {e}")
            raise

    except KeyError as e:
        logger.error(f"Missing configuration key: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
