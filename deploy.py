import os
os.system('git add . && git commit -am "`date +%F-%T` `git status -s`" && git push heroku master' )