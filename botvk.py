import vk_api
import config
from threading import Timer
from datetime import datetime
from datetime import timedelta
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotEvent,VkBotMessageEvent
from vk_api.utils import get_random_id

token = config.settings['TOKEN']
vktoken= config.settings['VKTOKEN']
group_id="214682553"
def get_delta(hour=0, minute=0, second=0, microsecond=0):
    now = datetime.now()
    run_at = now.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)
    if run_at < now:
        run_at += timedelta(days=1)

    return (run_at - now).total_seconds()

def getpost(dom,nom):
    post = getting_vk.wall.get(domain=dom)['items'][nom]
    owner_id = post['owner_id']
    media_id = post['id']
    attachment = f'wall{owner_id}_{media_id}'
    return attachment


def write_message(chat, message):
    authorize.method('messages.send', {'chat_id': chat, 'message': message, 'random_id': get_random_id()})

def write_repost(chat, message, attachment):
    authorize.method('messages.send',{'chat_id': chat, 'message': message, 'attachment': attachment, 'random_id': get_random_id()})

def checkat(chat,chek,name,num):
    print(chek,' i ',getpost(name, num))
    if chek!=getpost(name, num):
        print("пост1 изменен")
        attachment3 = getpost(name, num)
        write_repost(chat, "", attachment3)
        return 1
    else:print("совпал")



def send_msg(getting_api, chat_id, message):
    random_id = randint(1, 2147483647)

    getting_api.messages.send(
        random_id=random_id,
        chat_id=chat_id,
        message=message
    )

class CustomTimer:
    def __init__(self, *args, delta=0.0, function=checkat, interval=86400.0, **kwargs):
        self.delta = delta
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs

        self.timer = None

    def callback(self):
        ret=self.function(*self.args, **self.kwargs)
        self.normal_start()
        print(1)
        return ret


    def normal_start(self):
        ret=self.timer = Timer(self.interval, self.callback)
        self.timer.start()
        print(2)
        return ret

    def start(self):
        self.timer = Timer(self.delta, self.callback)
        self.timer.start()
        print(3)



#def repost_mes(message,object):
   #vk.method('wall.repost', {'message': message, 'object': object, 'group_id': 214682553,'random_id': get_random_id()})

authorize = vk_api.VkApi(token = token)
vk=vk_api.VkApi(token =vktoken)

getting_api = authorize.get_api()
getting_vk = vk.get_api()

longpoll = VkBotLongPoll(authorize, group_id="214682553")


#write_message(1, "Бот запущен!"),
print("Бот запущен!")
defaultmovie=getpost('themovieblog',1)
defaultmeme=getpost('thememeblog',0)
chek=getpost('testim1448',0)
print(chek)
delta = get_delta(22, 49)
t = CustomTimer(1, defaultmovie, 'themovieblog', 1, delta=delta, interval=3000)
t1 = t = CustomTimer(1, defaultmeme, 'thememeblog', 0, delta=delta, interval=2500)
t.start()
t1.start()
col=5
for event in longpoll.listen():
     if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text'):
        reseived_message = event.message.get('text')
        chat = event.chat_id
        print('из чата',chat)
        from_id = event.message.get('from_id')

     attachment1 = getpost('themovieblog', 1)
     attachment2 = getpost('thememeblog', 0)
   #  attachment3 = getpost('testim1448', 0)
     c=checkat(chat, defaultmovie,'themovieblog',1)
     c2=checkat(chat, defaultmeme,'thememeblog',0)
     if c==1:
         defaultmovie=getpost('themovieblog', 1)
     if c2==1:
         defaultmeme=getpost('thememeblog', 0)
     if reseived_message=="посты":
         write_message(chat,'введите количество отправляемых постов')
         col=1
     if col==1:
         col=reseived_message
     if  reseived_message == "член":
         print("пост1 отправлен в ", chat)
         write_message(chat,"последние 5 постов")
         for i in range(col):
             attachment1 = getpost('themovieblog', i)
             write_repost(chat,i, attachment1)

     if reseived_message == "мем":
        print("пост2 отправлен в ", chat)
        write_repost(chat, " ", attachment2)




