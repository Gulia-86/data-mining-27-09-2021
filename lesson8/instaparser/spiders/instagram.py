import scrapy
import re
import json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'   # Qw123456789
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1634577477:AWdQAK0AEOF+wFwWVYjoEuu8uCHn+Pabck9vUxQlFS3/o3VdiZCGuEm4HaF+MLP9EwSytUXe+VNGZWVqv/Pz+z14vr8gT4dClBa6OPYXzPbHCHcU0fUqrO731Bcf4OCxjIcxB4lurkTpWrZPz+Ir'
    user_for_parse = ['zefirka_izh', 'aptjukova']
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for i in self.user_for_parse:
                yield response.follow(
                    f'/{i}',
                    callback=self.f_parse,
                    headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                    cb_kwargs={'username': i}
                )

    def f_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12,
                     'max_id': 12}
        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
        url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'
        #https://i.instagram.com/api/v1/friendships/837544479/following/?count=12&max_id=12
        yield response.follow(url_followers,
                                callback=self.user_followers_parse,
                                headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                cb_kwargs={'username': username,
                                           'user_id': user_id,
                                           'variables': deepcopy(variables)}
                                )
        yield response.follow(url_following,
                              callback=self.user_following_parse,
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': variables}
                              )

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        users = j_data.get('users')
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&{urlencode(variables)}'
            yield response.follow(url_followers,
                                  callback=self.user_followers_parse,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)}
                                  )
        for user in users:
           follower_id=user.get('pk'),
           follower_username=user.get('username'),
           photo=user.get('profile_pic_url')
           item = InstaparserItem(user_id=user_id, username=username, relation = 'follower', follower_id = follower_id[0], follower_username=follower_username[0], photo=photo)

           yield item

    def user_following_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        users = j_data.get('users')
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&{urlencode(variables)}'
            yield response.follow(url_following,
                                  callback=self.user_following_parse,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': variables}
                                  )
        for user in users:
            following_id=user.get('pk'),
            following_username=user.get('username'),
            photo=user.get('profile_pic_url')
            item = InstaparserItem(user_id=user_id, username=username, relation = 'following', following_id = following_id[0], following_username=following_username[0], photo=photo)

            yield item



    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
