#! /usr/bin python
# -*- coding:utf-8 -*-

from django.test import TestCase
from sign.models import Event
from django.contrib.auth.models import User

class GuestManageTest(TestCase):
    """测试嘉宾管理"""

    def setUp(self):
        '''还是使用setUp初始化一些测试数据'''
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name='xiaomi5', limit=2000, address='beijing', status=1, start_time='2017-08-10 12:30:00')
        Guest.objects.create(realname='alen', phone=18611001100, email='alen@mail.com', sign=0, event_id=1)
        self.login_user = {'username':'admin', 'password':'admin123456'}

    def test_event_manage_success(self):
        '''测试嘉宾信息：alen'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'18611001100', response.content)

    def test_guest_manage_search_success(self):
        '''测试嘉宾搜索功能'''
        response = self.client.post('/login_action/', data=self.login_user)
        # 这里就是坑了，我们根据书中描述一步一步来得话，我们在views.py里定义的搜索功能是根据名字来搜索的，而不是根据手机号，下面应该修改为('/search_realname/', {'realname':'alen'})
        # response = self.client.post('/search_phone/', {'phone':'18611001100'})
        response = self.client.post('/search_realname/', {'realname':'alen'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'18611001100', response.content)

# class SignIndexActionTest(TestCase):
#     """测试发布会签到"""
#
#     def setUp(self):
#         User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
#         Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
#         Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen', status=1, start_time='2017-6-10 12:30:00')
#         Guest.objects.create(realname="alen", phone=18611001100, email='alen@mail.com', sign=0, event_id=1)
#         Guest.objects.create(realname="una", phone=18611011101, email='una@mail.com', sign=1, event_id=2)
#         self.login_user = {'username':'admin', 'password':'admin123456'}
#
#     def test_event_models(self):
#         '''测试添加的发布会数据'''
#         result1 = Event.objects.get(name='xiaomi5')
#         self.assertEqual(result1.address, 'beijing')
#         self.assertTrue(result1.status)
#         result2 = Event.objects.get(name='oneplus4')
#         self.assertEqual(result2.address, 'shenzhen')
#         self.assertTrue(result2.status)
#
#     def test_guest_models(self):
#         '''测试添加的嘉宾数据'''
#         result = Guest.objects.get(realname='alen')
#         self.assertEqual(result.phone, '18611001100')
#         self.assertEqual(result.event_id, 1)
#         self.assertFalse(result.sign)
#
#     def test_sign_index_action_phone_null(self):
#         '''测试手机号为空'''
#         response = self.client.post('/login_action/', data=self.login_user)
#         response = self.client.post('/sign_index_action/1/', {"phone":""})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"phone error.", response.content)
#
#     def test_sign_index_action_phone_or_event_id_error(self):
#         '''测试手机号或发布会id错误'''
#         response = self.client.post('/login_action/', data=self.login_user)
#         response = self.client.post('/sign_index_action/2/', {"phone":"18611001100"})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"event id or phone error.", response.content)
#
#     def test_sign_index_action_user_sign_has(self):
#         '''测试嘉宾已签到'''
#         response = self.client.post('/login_action/', data=self.login_user)
#         response = self.client.post('/sign_index_action/2/', {"phone":"18611011101"})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"user has sign in.", response.content)
#
#     def test_sign_index_action_sign_success(self):
#         '''测试嘉宾签到成功'''
#         response = self.client.post('/login_action/', data=self.login_user)
#         response = self.client.post('/sign_index_action/1/', {"phone":"18611001100"})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"sign in success!", response.content)