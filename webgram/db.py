import typing

if typing.TYPE_CHECKING:
    import webgram
    
class Db:
    
    async def set(self: 'webgram.BareServer',key, value):
        try:
            x = [i async for i in self.master.iter_messages(self.config.CONFIG_CHANNEL, search=key, limit=1) if i.message]
            if x :
                await x[0].message.edit(f"{key}:{value}")
                return True
            else:
                await self.client.send_message(self.config.CONFIG_CHANNEL,f"{key}:{value}")
                return True
        except Exception as e: 
            return e
               
    async def get(self: 'webgram.BareServer',key):
        async for i in self.master.iter_messages(self.config.CONFIG_CHANNEL, search=key, limit=1):
            try:
                if i :
                    value = i.message.split(":")[1]
                    return value
                else:
                    return None
            except Exception as e: 
                return e
           
    async def keys(self: 'webgram.BareServer'):
        keys = [i.message.split(":")[0] async for i in self.master.iter_messages(self.config.CONFIG_CHANNEL) if i.message]
        return keys
                
    async def values(self: 'webgram.BareServer'):
        values = [i.message.split(":")[1] async for i in self.master.iter_messages(self.config.CONFIG_CHANNEL) if i.message]
        return values
        
