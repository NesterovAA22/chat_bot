import logging
# изменения файла после комита
# и еще один комит
try:
    import settings
except ImportError:
    exit('нужно скопировать файл settings.py.default settings.py и указать token')
log = logging.getLogger("bot")

def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    file_handler = logging.FileHandler("bot.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    stream_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    log.setLevel(logging.DEBUG)




import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

#пушим насервер
#второй залив

class Bot:
    """
    ЭХО бот для vk.com
    версия Python 3.10"""

    def __init__(self, group_id, token):
        """
        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token
        self.vk =vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()



    def run(self):
        """"Запуск бота """
        for event in self.long_poller.listen():

            try:
                self.on_event(event=event)
            except Exception:
                log.exception("ошибка в обработке события")


    def on_event(self, event):
        """Оптравляет сообщение назад , если это сообщение текс
        :param event: VkBotMessageEvent object
        :return:None

        """
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            log.info("отправляем сообщение назад")
            message = event.message.text

            self.api.messages.send(user_id=event.message.from_id, message=message, random_id=random.randint(0, 2 ** 20))
        else:
            log.info("мы пока не умеем это обрабатывать:%s", event.type)



if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()