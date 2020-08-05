import os
import sys
import ast
from datetime import datetime

sys.path.append("./src/")

from firefox import Firefox
from unfollowers import Unfollowers

username = os.environ.get('INSTAGRAM_USERNAME')
password = os.environ.get('INSTAGRAM_PASSWORD')
headless = True if 'HEADLESS' not in os.environ else ast.literal_eval(
    os.environ.get('HEADLESS'))

print('[{}] Starting UP Instagram Unfollower Beak'.format(datetime.utcnow()))
if not os.environ.get('INSTAGRAM_USERNAME') or not os.environ.get('INSTAGRAM_PASSWORD'):
    sys.exit(
        'Please put INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD env vars')

print('[{}] Start build unfollowers don\'t following you'.format(datetime.utcnow()))

unfolloweres = Unfollowers()
unfollow_users_list = unfolloweres.make_list(username, password)

firefox_unfollower = Firefox()
firefox_unfollower.setup(headless, username, password)
firefox_unfollower.start_unfollow(unfollow_users_list)