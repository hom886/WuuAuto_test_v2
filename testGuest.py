from django.test import TestCase
from sign.models import Event, Guest
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
