from src.config import read_cfg
from src.parser import parse
from src.log import logger
from src.request import HTTPRequest
from src.send_sms import send_sms

import base64
import json

def main():
    cfg = read_cfg()
    sender, recipient, message = parse()

    logger.info(f"start sending: sender:{sender} recipient:{recipient}, message: {message}")

    auth = base64.b64encode(f"{cfg['username']}:{cfg['password']}".encode()).decode()
    content = json.dumps(
            {"sender": sender, 
             "recipient": recipient, 
             "message": message })

    request = HTTPRequest(
        method="POST",
        path="/send_sms",
        headers = 
            {"Host": f"{cfg['host']}",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
            "Content-Length": f"{len(content)}"},
        body = content
        
    )
    try:
        print(request.to_bytes().decode('utf-8'))
        response = send_sms(request, cfg['host'], cfg['port'])
        print(response.status_code, response.body)
        logger.info(f"Server response: {response.status_code} {response.status_message}\n{response.body}")
        
    except Exception as e:
        logger.error(f"HTTPRequest failed: {e}")





if __name__ == '__main__':
    main()