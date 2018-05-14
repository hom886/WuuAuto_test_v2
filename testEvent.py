from django.test import TestCase
from sign.models import Event
from django.contrib.auth.models import User

class EventManageTest(TestCase):
    """测试发布会管理"""

    def setUp(self):
        '''初始化测试数据，包括登录用户数据，发布会数据'''
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name='xiaomi5', limit=2000, address='beijing', status=1, start_time='2017-08-10 12:30:00')
        self.login_user = {'username':'admin', 'password':'admin123456'}    # 定义登录变量

    def test_event_manage_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'beijing', response.content)

    def test_event_manage_search_success(self):
        '''测试发布会搜索'''
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {'name':'xiaomi5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'beijing', response.content)