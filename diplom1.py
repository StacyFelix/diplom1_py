import json
import time
from pprint import pprint

import requests


class Object:
    token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class User(Object):

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return f"https://vk.com/id{str(self.user_id)}"

    def get_list_ids_friends(self):
        URL_API_VK = 'https://api.vk.com/method/friends.get'
        params = {'access_token': self.token, 'user_id': self.user_id, 'v': '5.52'}
        while True:
            print('_')
            try:
                response = requests.get(URL_API_VK, params=params)
            except:
                time.sleep(2)
                print('Error VkAPIError')
            else:
                res = response.json()
                if 'response' in res:
                    res_res = res['response']
                    if 'items' in res_res:
                        return res_res['items']
                    else:
                        return []
                else:
                    return []

    def get_list_ids_groups(self, extended='0'):
        URL_API_VK = 'https://api.vk.com/method/groups.get'
        params = {'access_token': self.token, 'user_id': self.user_id, 'v': '5.101', 'extended': extended,
                  'count': '1000'}
        while True:
            print('_')
            try:
                response = requests.get(URL_API_VK, params=params)
            except:
                time.sleep(2)
                print('Error VkAPIError')
            else:
                res = response.json()
                if 'response' in res:
                    res_res = res['response']
                    if 'items' in res_res:
                        return res_res['items']
                    else:
                        return []
                else:
                    return []

    def get_set_ids_groups_friends(self):
        # список друзей юзера
        list_ids_friends = self.get_list_ids_friends()
        len_list_ids_friends = len(list_ids_friends)

        # множество всех групп всех друзей юзера:
        set_ids_groups_friends = set()
        for id_friend in list_ids_friends:
            set_ids_groups_friends.update(set(User(id_friend).get_list_ids_groups('0')))
            print(f"Осталось друзей: {len_list_ids_friends}")
            len_list_ids_friends -= 1
        return set_ids_groups_friends

    def get_common_groups(self, param='diff'):
        # множество всех групп юзера:
        set_ids_groups = set(self.get_list_ids_groups('0'))

        # множество всех групп всех друзей юзера:
        set_ids_groups_friends = self.get_set_ids_groups_friends()

        print("Еще немного...")

        if param == 'diff':
            # разность множеств list_groups и list_groups_friends
            list_ids_groups = list(set_ids_groups.difference(set_ids_groups_friends))
            print(f"Список групп пользователя, в которых не состоят друзья\n{list_ids_groups}")
        elif param == 'intersec':
            # пересечение множеств list_groups и list_groups_friends
            list_ids_groups = list(set_ids_groups.intersection(set_ids_groups_friends))
            print(f"Список групп пользователя, в которых состоят друзья\n{list_ids_groups}")

        common_groups = []
        for id_group in list_ids_groups:
            group = dict()
            group_vk = Group(id_group)
            if bool(group_vk):
                group['name'] = group_vk['name']
                group['gid'] = group_vk['id']
                group['members_count'] = group_vk['members_count']
                common_groups.append(group)
        pprint(common_groups)

        if param == 'diff':
            with open("non_common_groups.json", "w", encoding='utf-8-sig') as datafile:
                json.dump(common_groups, datafile, ensure_ascii=False, indent=2)
        elif param == 'intersec':
            with open("common_groups.json", "w", encoding='utf-8-sig') as datafile:
                json.dump(common_groups, datafile, ensure_ascii=False, indent=2)


class Group(Object):

    def __new__(cls, group_id):
        URL_API_VK = 'https://api.vk.com/method/groups.getById'
        params = {'access_token': super().token, 'group_ids': group_id, 'v': '5.101', 'fields': ['members_count']}
        while True:
            try:
                response = requests.get(URL_API_VK, params=params)
            except:
                time.sleep(2)
                print('Error VkAPIError')
            else:
                res = response.json()
                if 'response' in res:
                    return res['response'][0]
                else:
                    return {}


if __name__ == '__main__':
    id_user = 171691064
    user_e = User(id_user)
    user_e.get_common_groups()
    # user_e.get_common_groups('intersec')
