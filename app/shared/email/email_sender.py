import logging
import smtplib
import ssl

from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailSender:
    """
    Envío de correos por SMTP.

    Sin SMTP_HOST configurado, en development el
    correo se escribe en el log para poder probar el
    flujo; en production no se envía y queda un error
    en el log.
    """

    @staticmethod
    def send(
        to: str,
        subject: str,
        body: str
    ) -> bool:

        if not settings.SMTP_HOST:

            if settings.APP_ENV == "production":
                logger.error(
                    "SMTP_HOST no configurado: no se envió "
                    "el correo '%s'.",
                    subject
                )
                return False

            logger.warning(
                "SMTP_HOST no configurado (development). "
                "Correo para %s | %s\n%s",
                to,
                subject,
                body
            )
            return True

        message = EmailMessage()
        message["From"] = settings.SMTP_FROM
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        try:

            if settings.SMTP_SECURITY == "SSL":
                server = smtplib.SMTP_SSL(
                    settings.SMTP_HOST,
                    settings.SMTP_PORT,
                    timeout=settings.SMTP_TIMEOUT_SECONDS,
                    context=ssl.create_default_context()
                )
            else:
                server = smtplib.SMTP(
                    settings.SMTP_HOST,
                    settings.SMTP_PORT,
                    timeout=settings.SMTP_TIMEOUT_SECONDS
                )

            with server:

                if settings.SMTP_SECURITY == "STARTTLS":
                    server.starttls(
                        context=ssl.create_default_context()
                    )

                if settings.SMTP_USERNAME:
                    server.login(
                        settings.SMTP_USERNAME,
                        settings.SMTP_PASSWORD
                    )

                server.send_message(message)

            return True

        except Exception:

            # No se registra el destinatario ni el cuerpo:
            # el cuerpo puede llevar un código válido.
            logger.exception(
                "No se pudo enviar el correo '%s'.",
                subject
            )
            return False
