import asyncio
import webgram
import aiohttp.web
import logging
from concurrent.futures import CancelledError
import signal

logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.DEBUG)

class AioHttpAppException(BaseException):
    """An exception specific to the AioHttp application."""


class GracefulExitException(AioHttpAppException):
    """Exception raised when an application exit is requested."""


class ResetException(AioHttpAppException):
    """Exception raised when an application reset is requested."""

def handle_sighup() -> None:
    logging.warning("Received SIGHUP")
    raise ResetException("Application reset requested via SIGHUP")


def handle_sigterm() -> None:
    logging.warning("Received SIGTERM")
    raise ResetException("Application exit requested via SIGTERM")


def cancel_tasks() -> None:
    for task in asyncio.Task.all_tasks():
        task.cancel()


def run():
	loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
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
	if __name__ == "__main__":
		try:
	        aiohttp.web.run_app(app,host="0.0.0.0", port=server.config.PORT, handle_signals=True)
	    except ResetException:
	        logging.warning("Reloading...")
	        cancel_tasks()
	        asyncio.set_event_loop(asyncio.new_event_loop())
	        return True
	    except GracefulExitException:
	        logging.warning("Exiting...")
	        cancel_tasks()
	        loop.close()
	return app
        
        
async def main():
    
    return run()
    #aiohttp.web.run_app(app,host="0.0.0.0", port=server.config.PORT)
    """"""


if __name__ == "__main__":
    run()