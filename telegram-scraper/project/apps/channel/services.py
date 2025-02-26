import logging
from uuid import uuid4

from constance import config
from django.conf import settings
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from apps import app
from apps.channel.models import Channel
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.message.models import Message

logger = logging.getLogger('django')


@app.task
def parsing_service_celery_wrapper():
    return ParsingService().process()


class ParsingService(AbstractService):
    def __init__(self):  # noqa: D107
        self.channels = Channel.objects.filter(is_active=True)

    def process(self, *args, **kwargs):
        client = TelegramClient(StringSession(config.SESSION_KEY), config.API_ID, config.API_HASH)
        client.connect()
        if not client.is_user_authorized():
            raise ValueError('Сессия сломалась...')
            # req = client.send_code_request(phone=config.PHONE, force_sms=False)
            # client.sign_in(config.PHONE, '', phone_code_hash=req.phone_code_hash)

        for channel in self.channels:
            self.process_channel(client=client, channel=channel)

        client.disconnect()

    def process_channel(self, client: TelegramClient, channel: Channel):
        for idx, message in enumerate(client.iter_messages(channel.link.replace('@', ''), limit=20)):  # noqa: WPS221
            logger.info(f'{idx} / {message.date} / канал {channel.link}...')  # noqa: WPS221
            messages = []

            db_message, created = Message.objects.get_or_create(
                ext_date=message.date,
                channel=channel,
                defaults={
                    'ext_id': message.id,
                    'link': f'https://t.me/{channel.link}/{message.id}',
                }
            )
            if message.message and not db_message.text:
                db_message.text = message.message
                db_message.save()

            if message.photo:
                filename = uuid4()
                message.download_media(f'{settings.MEDIA_ROOT}/{channel.link}/{filename}.jpg')  # noqa: WPS221 E501
                File.objects.create(file=f'{channel.link}/{filename}.jpg', message=db_message)

            # if message.document and message.document.mime_type == 'video/mp4':
            #     filename = uuid4()
            #     message.download_media(f'{settings.MEDIA_ROOT}/{channel.link}/{filename}.mp4')  # noqa: WPS221
            #     File.objects.create(file=f'{channel.link}/{filename}.mp4', message=db_message)  # noqa: WPS221 E501

            messages.append(db_message)

        # Удалить сообщения без text
        for message in Message.objects.all():
            if not message.text:
                message.delete()
