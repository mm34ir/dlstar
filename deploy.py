import os
os.system('git add . && git commit -am "`date +%F-%T`" && git commit --amend -m "`git log -1 -p`"  && git push heroku master' )