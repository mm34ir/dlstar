import os 

class Config:
    # noinspection PyPep8Naming
    class config:
        APP_ID = 50807

        API_HASH = "21ab7cb0a453b5e60016dc7bbeb701cb"

        SESS_NAME = "dlstar_bot_client"
        
        BOT_TOKEN = "1215711283:AAFuct-4Kd1-cDaWp4rLENN08oxgNSOx7FI"

        channel = 'UserlandApp'

        STATS_CHANNEL = -1001249461809

        HOST = "127.0.0.1"

        PORT = os.getenv('PORT')

        ROOT_URI = f"https://dlstarus.dlgram.ml"

        ROOT_URI_2 = "https://dlstarir.dlgram.ml"

        ENCODING = "utf8"


        # ALLOWED_EXT = ["mkv", "mp4", "flv"]
