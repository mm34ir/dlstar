import sqlite3
from os import path

import typing

if typing.TYPE_CHECKING:
    import webgram


class Db:
    class Kv(dict):
        async def __init__(self: 'webgram.BareServer', filename=None,autocommit=None):
            self.cfile = filename
            if path.exists(filename):
                self.conn = sqlite3.connect(self.cfile)
            else:
                async for i in self.master.iter_messages(self.config.STATS_CHANNEL, search=self.cfile, limit=1):
                    if i :
                        await self.master.download_media(i)
                    else :
                        self.conn = sqlite3.connect(self.cfile)
                    
            self.conn.execute("CREATE TABLE IF NOT EXISTS kv (key text unique, value text)")
            self.autocommit = autocommit
    
        def close(self: 'webgram.BareServer'):
            self.commit()
            self.conn.close()
        
        def commit(self: 'webgram.BareServer'):
            self.conn.commit()
            self.master.send_file(self.config.STATS_CHANNEL,self.cfile)
    
        def __len__(self: 'webgram.BareServer'):
            rows = self.conn.execute('SELECT COUNT(*) FROM kv').fetchone()[0]
            return rows if rows is not None else 0
    
        def iterkeys(self: 'webgram.BareServer'):
            c = self.conn.cursor()
            for row in self.conn.execute('SELECT key FROM kv'):
                yield row[0]
    
        def itervalues(self: 'webgram.BareServer'):
            c = self.conn.cursor()
            for row in c.execute('SELECT value FROM kv'):
                yield row[0]
    
        def iteritems(self: 'webgram.BareServer'):
            c = self.conn.cursor()
            for row in c.execute('SELECT key, value FROM kv'):
                yield row[0], row[1]
    
        def keys(self: 'webgram.BareServer'):
            return list(self.iterkeys())
    
        def values(self: 'webgram.BareServer'):
            return list(self.itervalues())
    
        def items(self: 'webgram.BareServer'):
            return list(self.iteritems())
    
        def __contains__(self: 'webgram.BareServer', key):
            return self.conn.execute('SELECT 1 FROM kv WHERE key = ?', (key,)).fetchone() is not None
    
        def __getitem__(self: 'webgram.BareServer', key):
            item = self.conn.execute('SELECT value FROM kv WHERE key = ?', (key,)).fetchone()
            if item is None:
                raise KeyError(key)
            return item[0]
    
        def __setitem__(self: 'webgram.BareServer', key, value):
            self.conn.execute('REPLACE INTO kv (key, value) VALUES (?,?)', (key, value))
            if self.autocommit:
                return self.commit()
    
        def __delitem__(self: 'webgram.BareServer', key):
            if key not in self:
                raise KeyError(key)
            self.conn.execute('DELETE FROM kv WHERE key = ?', (key,))
            if self.autocommit:
                return self.commit()
    
        def __iter__(self: 'webgram.BareServer'):
            return self.iterkeys()
    