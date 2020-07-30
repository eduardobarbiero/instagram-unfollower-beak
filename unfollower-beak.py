import os
import sys
import ast
from datetime import datetime

sys.path.append("./src/")

from firefox import Firefox

instagram_website = 'https://www.instagram.com/accounts/login'
username = os.environ.get('INSTAGRAM_USERNAME')
password = os.environ.get('INSTAGRAM_PASSWORD')
enc_password = '#PWD_INSTAGRAM_BROWSER:0:1590954226:' + str(os.environ.get('INSTAGRAM_PASSWORD')) # IF need crypt password
headless = True if 'HEADLESS' not in os.environ else ast.literal_eval(os.environ.get('HEADLESS'))

cache_dir = 'cache'
i_will_unfollow = '%s/i_will_unfollow.json' % (cache_dir)
firefox_binary_path = '/usr/bin/firefox'

print('[{}] Starting UP Instagram Unfollower Beak'.format(datetime.utcnow()))

unfollower = Firefox()
unfollower.setUp(headless, firefox_binary_path)
unfollower.openWebsite(instagram_website)
unfollower.makeLogin(username, password)
unfollower.disableNotifiers()
i_will_unfollow_list = unfollower.loadProfilesToUnfollow(i_will_unfollow)
unfollower.unfollowList(i_will_unfollow_list)
unfollower.closeWebsite()