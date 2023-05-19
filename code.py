import vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import os
from config import main_token
from threading import Thread
import dbtests
import chat
import creat_img

vk_session = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(vk_session, 207959338)
print('pohui')
x = 0


def sender(id, text, ):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def get_url(id):
    return vk_session.method('users.get', {'user_ids': id, 'fields': 'photo_100'})[0]['photo_100']


def deleter(count):
    os.remove('rectangle' + str(count) + '.jpg')
    os.remove('img' + str(count) + '.jpg')


def send_image(id, count):
    a = vk_session.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open('rectangle' + str(count) + '.jpg', 'rb')}).json()
    c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[
        0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])
    vk_session.method("messages.send", {'chat_id': id, "attachment": d, "random_id": 0})
    deleter(count)


def main(eventy, count):
    y = random.randint(1, 10000)
    msg = eventy.object.message['text'].lower()
    id = eventy.chat_id
    if dbtests.select_with_fetchone(eventy.object.message['from_id']) is None:
        dbtests.new_user(eventy.object.message['from_id'])
    if msg == '/игра':
        if dbtests.select_with_fetchone(eventy.object.message['from_id'])[2] >= 50:
            sender(id, 'Ваша ставка 50$')
            dbtests.update(-50, eventy.object.message['from_id'])
            if y == 3:
                sender(id, 'Ты проиграл.Соси)')
            else:
                dbtests.update(100, eventy.object.message['from_id'])
                sender(id, 'Ты выиграл 100 $.Молодец, лови хуец.')
        else:
            sender(id, 'Насоси, потом проси.')
    if msg == '/цвд':
        text = eventy.object.message['reply_message']['text']
        if len(text) < 80:
            user_id = eventy.object.message['reply_message']['from_id']
            first_name = vk_session.method('users.get', {'user_ids': user_id, 'fields': 'first_name'})[0]['first_name']
            name = vk_session.method('users.get', {'user_ids': user_id, 'fields': 'last_name'})[0][
                       'last_name'] + ' ' + first_name
            url = get_url(user_id)
            creat_img.get_img(url, text, name, count)
            send_image(id, count)
        else:
            sender(id, "Ты блядь долбаёб? Нахуй тебе такая длинная цитата?")


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            x += 1
            Thread(target=main, args=(event, x), daemon=True).start()
            print('pohui')
