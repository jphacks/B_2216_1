from dotenv import load_dotenv, dotenv_values

load_dotenv(verbose=True)
values = dotenv_values(verbose=True)

DATABASE_URI = values['DATABASE_URI']

APNS_DOMAIN = values['APNS_DOMAIN'] or ''
APNS_TOPIC = values['APNS_TOPIC'] or ''
CL_CERT_PATH = values['CL_CERT_PATH'] or ''