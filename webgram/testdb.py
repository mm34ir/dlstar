from mrdb import DB

class musa(DB):
    def __init__(self):
        self.db = self.KV("test.db",True)
    def set(self,key,value):
        self.db[key] = value
        return self.db[key] 
        
t = musa()
t.set("key","musa")