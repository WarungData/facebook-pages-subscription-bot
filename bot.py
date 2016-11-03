import telepot
import pyrebase
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import requests
import time
import datetime
import settings

firebase = pyrebase.initialize_app(settings.config)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    buttons = [[(KeyboardButton(text='BuzzFeed')), (KeyboardButton(text='9GAG'))],
               [(KeyboardButton(text='Done Subscribing'))]
               ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

    db = firebase.database()
    data = {"chat_id": chat_id, "subscriptions": []}
    chats = db.child("chats").order_by_child("chat_id").equal_to(chat_id).get()
    if len(chats.pyres) == 0:
        db.child("chats").push(data)
        chats = db.child("chats").order_by_child("chat_id").equal_to(chat_id).get()

    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, 'To subscribe, enter /subscribe')
        elif msg['text'] == '/subscribe':
            bot.sendMessage(chat_id, 'Welcome', reply_markup=keyboard)
        elif msg['text'] in settings.pages_dict.keys():
            for chat in chats.each():
                if 'subscriptions' in chat.val():
                    chat.val()['subscriptions'].append(msg['text'])
                    subscriptions = chat.val()['subscriptions']
                else:
                    subscriptions = [msg['text']]

                db.child("chats").child(chat.key()).update({"subscriptions": subscriptions})
            bot.sendMessage(chat_id, 'Any more to subscribe?', reply_markup=keyboard)

        elif msg['text'] == 'Done Subscribing':
            bot.sendMessage(chat_id, 'You will now be able to receive new updates from us!')
        else:
            bot.sendMessage(chat_id, 'Want to /subscribe?')


def get_all_chats():
    db = firebase.database()
    chats = db.child("chats").get()

    return chats.each()


bot = telepot.Bot(settings.BOT_TOKEN)
bot.message_loop(handle)
print('Listening ...')


def dispatch_posts():
    yesterday = datetime.date.today() - datetime.timedelta(hours=1)
    unix_time = yesterday.strftime("%s")

    for page, page_id in settings.pages_dict.items():
        request = 'https://graph.facebook.com/v2.8/' + page_id + '/posts?access_token=' + settings.fb_app_id + '|' + settings.fb_app_secret + '&since=' + unix_time
        r = requests.get(request)
        json_data = r.json()['data']

        if len(json_data) > 0:
            chats = get_all_chats()
            post_ids = ','.join(str(e) for e in [post['id'] for post in json_data])

            request = 'https://graph.facebook.com/v2.8/?ids=' + ''.join(
                post_ids) + '&access_token=' + settings.fb_app_id + '|' + settings.fb_app_secret + '&fields=message,picture,permalink_url,description'
            posts = requests.get(request).json()

            for chat in chats:
                for key, value in posts.items():
                    if 'subscriptions' in chat.val().keys() and page in chat.val()['subscriptions']:
                        bot.sendMessage(chat.val()['chat_id'], value['permalink_url'] + '\n\n' + value['message'],
                                        disable_web_page_preview=False)

    print('Done dispatch one round')


# Keep the program running.
while 1:
    time.sleep(settings.poll_interval)
    dispatch_posts()
