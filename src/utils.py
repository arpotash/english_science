import abc
import csv
import typing as t
from datetime import datetime, timezone, timedelta
from io import StringIO

import httpx
import jwt
import fastapi_mail

from src.models import Word
from src.schemas.lesson import CsvFileColumns
from src.settings.settings import Config
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token:

    @staticmethod
    def encode_auth_token(login: str) -> str:
        message = {
            'iss': login,
            'exp': datetime.now(timezone.utc) + timedelta(hours=10)
        }
        return jwt.encode(message, Config.AUTH_SECRET_KEY, algorithm=Config.AUTH_ALGORITHM)

    @staticmethod
    def encode_verification_token(login: str) -> str:
        message = {
            'iss': login,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(message, Config.VERIFY_SECRET_KEY, algorithm=Config.AUTH_ALGORITHM)


    @staticmethod
    def decode_auth_token(token: str) -> dict:
        return jwt.decode(token, key=Config.AUTH_SECRET_KEY, algorithms=[Config.AUTH_ALGORITHM])


async def send_mail(email: str, token: str) -> None:
    template = f"""
    <html>
    <body>
        <p>Пройдите верификацию электронной почты
            <br>Пройдите по <a href="{Config.EMAIL_VERIFICATION_URL}?access_token={token}">ссылке</a> для прохождения верификации</p>
    </body>
    </html>
    """
    message = fastapi_mail.MessageSchema(
        subject='Верификация нового пользователя',
        recipients=[email],
        body=template,
        subtype=fastapi_mail.MessageType('html')
    )
    fm = fastapi_mail.FastMail(Config.MAIL_SENDING_CONFIG)
    await fm.send_message(message)


class Password:

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

class UnitParams:

    @staticmethod
    def calculate_gag_index(words_sequence: list[Word]) -> float:
        words, syllables = [], []
        for element in words_sequence:
            if len(element.title.split('_')) > 1:
                syllables.append(element)
            else:
                words.append(element)

        return 206.835 - 1.015 * (len(words) / 1) - 84.6 * (len(syllables) / len(words))

    @staticmethod
    def calculate_diversity_index(words_sequence: list) -> float:
        word_names_lst = [word.title for word in words_sequence]
        total_words = len(word_names_lst)
        unique_words = len(set(word_names_lst))

        return 0 if total_words == 0 else unique_words / total_words


class FileManager(abc.ABC):

    @abc.abstractmethod
    def read(self, file_name: str) -> t.NoReturn:
        raise NotImplemented


class CsvFileManager(FileManager):

    @classmethod
    def read(cls, file_content: str) -> list:
        words = []

        csv_data = csv.DictReader(StringIO(file_content))


        for row in csv_data:
            word_title, topic = row.get("Term"), row.get('Category')
            words.append(CsvFileColumns(title=word_title, topic=topic))

            if len(words) >= 20:
                break

        return words

class OxfordApi:

    @classmethod
    async def parse_word_from_api(cls, title: str) -> dict | None:

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{Config.ENGLISH_VOCABULAR_URL}/{title}',
                params={'key': Config.ENGLISH_VOCABULAR_API_KEY}
            )

            if response.status_code == 200:
                response_json = response.json()

                if isinstance(response_json, list) and isinstance(response_json[0], dict) and response_json[0].get('meta'):
                    return response_json[0]


    @classmethod
    def get_meaning(cls, meta: dict) -> str:
        return meta['shortdef'][0] if isinstance(meta.get('shortdef'), list) else meta['shortdef']

    @classmethod
    def get_synonyms(cls, meta: dict) -> list[str]:
        return meta['meta']['syns'][0] if meta['meta']['syns'] else []