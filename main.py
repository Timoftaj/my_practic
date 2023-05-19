import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import main_token
from threading import Thread


vk_session = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(vk_session, 207959338)



def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def main(eventy):
    msg = eventy.object.message['text'].lower()
    id = eventy.chat_id
    sender(id, msg)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            main(event)

