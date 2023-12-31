import os

from fastapi_mail import ConnectionConfig


class SMPTEnvs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAILS_TO = os.getenv("MAILS_TO").split(",")
    MAIL_STARTTLS = bool(int(os.getenv("MAIL_STARTTLS")))
    MAIL_SSL_TLS = bool(int(os.getenv("MAIL_SSL_TLS")))
    USE_CREDENTIALS = bool(int(os.getenv("USE_CREDENTIALS")))
    MESSAGE = """<p>Witaj, nastąpiła zmiana w planie zajęć.</p>
                <p>Powodzenia!</p>
                <br></br>
                Plik w załączniku.
                """


conf = ConnectionConfig(
    MAIL_USERNAME=SMPTEnvs.MAIL_USERNAME,
    MAIL_PASSWORD=SMPTEnvs.MAIL_PASSWORD,
    MAIL_FROM=SMPTEnvs.MAIL_FROM,
    MAIL_PORT=SMPTEnvs.MAIL_PORT,
    MAIL_SERVER=SMPTEnvs.MAIL_SERVER,
    MAIL_STARTTLS=SMPTEnvs.MAIL_STARTTLS,
    MAIL_SSL_TLS=SMPTEnvs.MAIL_SSL_TLS,
    USE_CREDENTIALS=SMPTEnvs.USE_CREDENTIALS,
    MAIL_DEBUG=1,
)
