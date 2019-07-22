import json
import time
from pprint import pprint

import requests


class Object:
    token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

    def get_params(self):
        return {
            'access_token': self.token
        }


class User(Object):

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return f"https://vk.com/id{str(self.user_id)}"

    def get_list_ids_friends(self):
        URL_API_VK = 'https://api.vk.com/method/friends.get'
        params = self.get_params()
        params['user_id'] = self.user_id
        params['v'] = '5.52'
        while(True):
            print('_')
            try:
                response = requests.get(URL_API_VK, params=params)
            except:
                time.sleep(1)
                print('Error VkAPIError из get_list_ids_friends')
            else:
                return response.json()['response']['items']

    def get_list_ids_groups(self, extended):
        # URL_API_VK = 'https://api.vk.com/method/users.getSubscriptions'
        URL_API_VK = 'https://api.vk.com/method/groups.get'
        params = self.get_params()

        params['user_id'] = self.user_id
        params['v'] = '5.101'
        params['extended'] = extended
        params['count'] = '1000'

        while(True):
            print('_')
            try:
                response = requests.get(URL_API_VK, params=params)
            except:  # VkAPIError
                time.sleep(1)
                print('Error VkAPIError из get_list_ids_groups')

            try:
                res = response.json().get('response').get('items')
            except:
                return []
            else:
                return res

    def get_json_non_common_groups(self):
        # множество всех групп юзера:
        set_ids_groups = set(self.get_list_ids_groups('0'))

        # список друзей юзера
        list_ids_friends = self.get_list_ids_friends()

        # множество всех групп всех друзей юзера:
        set_ids_groups_friends = set()
        for id_friend in list_ids_friends:
            set_ids_groups_friends.update(set(User(id_friend).get_list_ids_groups('0')))

        # разность множеств list_groups и list_groups_friends
        list_ids_res_groups = list(set_ids_groups.difference(set_ids_groups_friends))
        print(list_ids_res_groups)

        group_el = Group()

        # не работает:
        # pprint(group.get_group_by_id(list_ids_res_groups))

        # поэтому вот так:
        json_non_common_groups = []
        for id_group in list_ids_res_groups:
            group = dict()
            group_vk = group_el.get_group_by_id(id_group)[0]
            group['name'] = group_vk['name']
            group['gid'] = group_vk['id']
            group['members_count'] = group_vk['members_count']
            json_non_common_groups.append(group)

        pprint(json_non_common_groups)

        with open("non_common_groups.json", "w", encoding='utf-8-sig') as datafile:
            json.dump(json_non_common_groups, datafile, ensure_ascii=False, indent=2)


class Group(Object):

    def get_group_by_id(self, group_id):
        URL_API_VK = 'https://api.vk.com/method/groups.getById'
        params = self.get_params()
        params['group_ids'] = group_id
        params['v'] = '5.101'
        params['fields'] = ['members_count']
        while(True):
            try:
                response = requests.get(URL_API_VK, params=params)
            except: #VkAPIError
                time.sleep(1)
                print('VkAPIError из get_group_by_id')
            else:
                return response.json().get('response')


# ids_groups = [134709480, 125927592, 101522128, 8564]
# for id_group in ids_groups:
#     group_el = Group()
#     pprint(group_el.get_group_by_id(id_group))

# group_e = Group()
# pprint(group_e.get_group_by_id(ids_groups))

id_user = 171691064
user_e = User(id_user)
user_e.get_json_non_common_groups()
