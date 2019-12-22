from pixivpy3 import *
import math
import getpass
import json

aapi = AppPixivAPI()
papi = PixivAPI()
entries_per_page = 30
data = {}

def login():
    username = input('Enter your username: ')
    password = getpass.getpass('Enter your password: ')
    aapi.login(username, password)
    papi.login(username, password)

def export_following_users():    
    user_id = int(input('Enter user ID: '))

    json_result = aapi.user_detail(user_id)
    follow_user_num = json_result['profile']['total_follow_users']
    page_num = math.ceil(follow_user_num / entries_per_page)
    user_list = []
    for i in range(page_num):
        json_result = aapi.user_following(user_id, offset=i*entries_per_page)
        for j in range(entries_per_page):
            try: 
                user_list.append(json_result['user_previews'][j]['user']['id'])
            except IndexError:
                break

    data['following_users'] = user_list

def export_bookmarks():
    user_id = int(input('Enter user ID: '))

    bookmark_list = []
    bookmark_id = None
    json_result = aapi.user_bookmarks_illust(user_id, max_bookmark_id=bookmark_id)
    while (json_result['illusts']):
        for illust in json_result['illusts']:
            bookmark_list.append(illust['id'])
        if json_result['next_url']:
            bookmark_id = aapi.parse_qs(json_result['next_url'])['max_bookmark_id']
            json_result = aapi.user_bookmarks_illust(user_id, max_bookmark_id=bookmark_id)
        else:
            break

    data['bookmarks'] = bookmark_list

def import_from_file(filename):
    with open(filename, 'r') as f:
        global data
        data = json.load(f)

def follow_users():
    for user_id in data['following_users']:
        papi.me_favorite_users_follow(user_id)

def add_bookmarks():
    for artwork_id in data['bookmarks']:
        aapi.illust_bookmark_add(artwork_id)

def store_results(filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

