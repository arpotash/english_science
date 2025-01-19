import os
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import SecretStr


class Config:
    SQLALCHEMY_ISOLATION_LEVEL = os.getenv('SQLALCHEMY_ISOLATION_LEVEL') or 'READ_COMMITTED'
    AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    VERIFY_SECRET_KEY = os.getenv('VERIFY_SECRET_KEY')
    AUTH_ALGORITHM = os.getenv('AUTH_ALGORITHM')
    EMAIL_VERIFICATION_URL = os.getenv('EMAIL_VERIFICATION_URL')
    DB_HOST = os.getenv('DB_HOST')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME')
    DB_URI = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    ENGLISH_VOCABULAR_URL = os.getenv('ENGLISH_VOCABULAR_URL')
    ENGLISH_VOCABULAR_API_KEY = os.getenv('ENGLISH_VOCABULAR_API_KEY')
    MAIL_SENDING_CONFIG = ConnectionConfig(
        MAIL_FROM=os.getenv('SERVER_MAIL_USERNAME'),
        MAIL_USERNAME=os.getenv('SERVER_MAIL_USERNAME'),
        MAIL_PASSWORD=SecretStr(os.getenv('SERVER_MAIL_PASSWORD')),
        MAIL_PORT=587,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_SSL_TLS=False,
        MAIL_STARTTLS=True,
    )
