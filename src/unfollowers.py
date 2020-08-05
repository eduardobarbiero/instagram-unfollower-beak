import sys
import time
import random
import requests
import pickle
import json
import re

from datetime import datetime

instagram_url = 'https://www.instagram.com'
login_route = '%s/accounts/login/ajax/' % (instagram_url)
logout_route = '%s/accounts/logout/' % (instagram_url)
profile_route = '%s/%s/'
query_route = '%s/graphql/query/' % (instagram_url)


class Unfollowers(object):
    session = None

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        self.session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })

        self.session.cookies.update({
            'ig_pr': '1',
            'ig_vw': '1920',
        })

        reponse = self.session.get(instagram_url)
        if 'csrftoken' in reponse.cookies:
            self.session.headers.update({
                'X-CSRFToken': reponse.cookies['csrftoken']
            })
        else:
            print('[{}] No csrf token found'.format(datetime.utcnow()))
            return False

        time.sleep(random.randint(2, 6))

        post_data = {
            'username': username,
            'enc_password': '#PWD_INSTAGRAM_BROWSER:0:1590954226:' + password
        }

        response = self.session.post(
            login_route, data=post_data, allow_redirects=True)
        response_data = json.loads(response.text)

        if 'two_factor_required' in response_data:
            print(
                '[{}] Disable 2-factor authentication to login'.format(datetime.utcnow()))
            sys.exit(1)

        if response_data['authenticated']:
            self.session.headers.update({
                'X-CSRFToken': response.cookies['csrftoken']
            })

        return response_data['authenticated']

    def get_user_profile(self, username):
        response = self.session.get(profile_route % (instagram_url, username))
        extract = re.search(
            r'window._sharedData = (.+);</script>', str(response.text))
        response = json.loads(extract.group(1))
        return response['entry_data']['ProfilePage'][0]['graphql']['user']

    def get_followers_list(self):
        followers_list = []

        query_hash = '56066f031e6239f35a904ac20c9f37d9'
        variables = {
            "id": self.session.cookies['ds_user_id'],
            "include_reel": False,
            "fetch_mutual": False,
            "first": 50
        }

        print('[{}] Building Followers users'.format(datetime.utcnow()))

        response = self.session.get(query_route, params={
                                    'query_hash': query_hash, 'variables': json.dumps(variables)})
        while response.status_code != 200:
            time.sleep(600)
            response = self.session.get(query_route, params={
                                        'query_hash': query_hash, 'variables': json.dumps(variables)})

        response = json.loads(response.text)

        for edge in response['data']['user']['edge_followed_by']['edges']:
            followers_list.append(edge['node'])

        while response['data']['user']['edge_followed_by']['page_info']['has_next_page']:
            variables['after'] = response['data']['user']['edge_followed_by']['page_info']['end_cursor']

            time.sleep(2)

            response = self.session.get(query_route, params={
                                        'query_hash': query_hash, 'variables': json.dumps(variables)})
            while response.status_code != 200:
                time.sleep(600)
                response = self.session.get(query_route, params={
                                            'query_hash': query_hash, 'variables': json.dumps(variables)})

            response = json.loads(response.text)

            for edge in response['data']['user']['edge_followed_by']['edges']:
                followers_list.append(edge['node'])

        print('[{}] Done build followers users'.format(datetime.utcnow()))

        return followers_list

    def get_following_list(self):
        follows_list = []

        query_hash = 'c56ee0ae1f89cdbd1c89e2bc6b8f3d18'
        variables = {
            "id": self.session.cookies['ds_user_id'],
            "include_reel": False,
            "fetch_mutual": False,
            "first": 50
        }

        print('[{}] Building Following users'.format(datetime.utcnow()))

        response = self.session.get(query_route, params={
                                    'query_hash': query_hash, 'variables': json.dumps(variables)})
        while response.status_code != 200:
            time.sleep(600)
            response = self.session.get(query_route, params={
                                        'query_hash': query_hash, 'variables': json.dumps(variables)})

        response = json.loads(response.text)

        for edge in response['data']['user']['edge_follow']['edges']:
            follows_list.append(edge['node'])

        while response['data']['user']['edge_follow']['page_info']['has_next_page']:
            variables['after'] = response['data']['user']['edge_follow']['page_info']['end_cursor']

            time.sleep(2)

            response = self.session.get(query_route, params={
                                        'query_hash': query_hash, 'variables': json.dumps(variables)})
            while response.status_code != 200:
                time.sleep(600)
                response = self.session.get(query_route, params={
                                            'query_hash': query_hash, 'variables': json.dumps(variables)})

            response = json.loads(response.text)

            for edge in response['data']['user']['edge_follow']['edges']:
                follows_list.append(edge['node'])

        print('[{}] Done build following users'.format(datetime.utcnow()))

        return follows_list

    def logout(self):
        post_data = {
            'csrfmiddlewaretoken': self.session.cookies['csrftoken']
        }

        self.session.post(logout_route, data=post_data)

    def make_not_following_you(self, following_list, followers_list):
        followers_usernames = {user['username'] for user in followers_list}
        unfollow_users_list = [
            user for user in following_list if user['username'] not in followers_usernames]

        print('[{}] You following but those don\'t follow you: {}'.format(
            datetime.utcnow(), len(unfollow_users_list)))

        return unfollow_users_list

    def make_list(self, username, password):
        is_logged = self.login(username, password)
        if is_logged == False:
            sys.exit('Login failed')

        time.sleep(random.randint(2, 4))

        connected_user = self.get_user_profile(username)
        print('[{}] Logged as {} ({} followers and following {})'.format(datetime.utcnow(
        ), connected_user['username'], connected_user['edge_followed_by']['count'], connected_user['edge_follow']['count']))

        time.sleep(random.randint(2, 4))

        following_list = self.get_following_list()
        followers_list = self.get_followers_list()

        unfollow_users_list = self.make_not_following_you(
            following_list, followers_list)

        self.logout()

        return unfollow_users_list
