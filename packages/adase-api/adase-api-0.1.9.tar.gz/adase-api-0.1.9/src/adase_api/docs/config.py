import os


class AdaApiConfig:
    AUTH_HOST = os.environ.get('AUTH_API_HOST', "https://adalytica.io/user-identity/auth")
    HOST_KEYWORD = os.environ.get('ADA_API_KEYWORD_HOST', "http://api-keyword.adalytica.io")
    HOST_TOPIC = os.environ.get('ADA_API_TOPIC_HOST', "http://api.adalytica.io")
    PORT = os.environ.get('ADA_API_PORT', "80")
    USERNAME = os.environ.get('ADA_API_USERNAME', "")
    PASSWORD = os.environ.get('ADA_API_PASSWORD', "")
    DEFAULT_DAYS_BACK = int(os.environ.get('DEFAULT_DAYS_BACK', "183"))
