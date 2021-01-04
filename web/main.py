import asyncio
import webgram
import aiohttp.web
import logging
from concurrent.futures import CancelledError
import signal

logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()

server = webgram.BareServer(loop)
app = aiohttp.web.Application(client_max_size=1024*1024*20)
app.add_routes([
    aiohttp.web.get('/', server.hello),
    aiohttp.web.get('/m3u/{peer}', server.grab_m3u),
    aiohttp.web.get('/watch/{peer}/{mid}/{name}', server.watch_stream),
    aiohttp.web.get('/watch/{hash}', server.watch_stream),
    aiohttp.web.get('/w/{h}/{name}', server.watch_stream),
    aiohttp.web.get('/w/{h}', server.watch_stream),
    aiohttp.web.get('/watch/{hash}/{name}', server.watch_stream),
    aiohttp.web.get('/test_upload', server.test_upload),
    aiohttp.web.post('/upload_big', server.upload_big),
    aiohttp.web.post('/upload', server.upload),

])
        
        
async def main():
    return app


if __name__ == "__main__":
            aiohttp.web.run_app(app,host="0.0.0.0", port=server.config.PORT, handle_signals=True)
            