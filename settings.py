BOT_TOKEN = 'XXXXXX'  # get token from telegram BotFather

# please get these info from firebase for storing user subscriptions
config = {
    "apiKey": "XXXXX",
    "authDomain": "XXX.firebaseapp.com",
    "databaseURL": "https://XXX.firebaseio.com",
    "storageBucket": "XXX.appspot.com",
    "serviceAccount": "./XXX.json" # you will need to create an service account from firebase, please refer to pyrebase doc
}

# please create an app in FB so you will be able to use FB Graph API to crawl facebook pages
fb_app_id = 'XXXXXX'
fb_app_secret = 'XXXXXX'

# These are the pages that you will support subscriptions, you will need to update the keyboard layout as well
pages_dict = {'BuzzFeed': 'BuzzFeed',
              '9GAG': '9gag'}

# how frequent do you poll all these pages (in seconds)
poll_interval = 3600
