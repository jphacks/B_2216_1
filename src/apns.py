import httpx
import json
from .env_vars import APNS_TOPIC, APNS_DOMAIN, CL_CERT_PATH
import logging

client = httpx.Client(http2=True, cert=CL_CERT_PATH)
HEADERS = {'apns-topic': APNS_TOPIC}
logger = logging.getLogger('APNs handler')


def call_apns_api(device_id: str, title: str, body: str):
    '''
    Call APNs (Apple's Push Notification service) API
    '''
    full_url = f'https://{APNS_DOMAIN}/3/device/{device_id}'
    payload_dict = {
        'aps': {
            'alert': {
                'title': title,
                'body': body
            },
            'sound': 'default'
        }
    }
    res = client.post(full_url, json=payload_dict, headers=HEADERS)
    if res.status_code != 200:
        logger.error(res, res.content)
    else:
        logger.info(res, res.content)
    return res
