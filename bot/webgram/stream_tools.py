from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import MessageMediaDocument, InputMessagesFilterDocument
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import Document
from telethon.tl.types import Message
from telethon.tl.types.messages import MessagesNotModified
import base64
from telethon import events
from telethon.tl.custom import Message
import typing
import werkzeug.utils
import re
from typing import Tuple, Union
if typing.TYPE_CHECKING:
    import webgram


class StreamTools:

    @staticmethod
    def Find(string): 
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)       
        return [x[0] for x in url] 

    @staticmethod
    def encode(clear):
        key="musa"
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()
    
    @staticmethod
    def decode(enc):
        key="musa"
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
        
    @staticmethod
    def size(siz):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if siz < 1024.0:
                return "%3.1f %s" % (siz, x)
            siz /= 1024.0
        return siz

    @staticmethod
    def get_file_name(message: Union[Message, events.NewMessage.Event]) -> str:
        if message.file.name:
            return message.file.name
        ext = message.file.ext or ""
        return f"{message.date.strftime('%Y-%m-%d_%H-%M-%S')}{ext}"
