import os
os.system('git add . && git commit -am "`git log -1 -p`" && git push heroku master' )