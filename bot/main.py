import asyncio
import webgram
import logging

logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
server = webgram.BareServer(loop)
loop.run_forever()
