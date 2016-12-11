from chat.chat import app

from flask import Flask
from flask_testing import TestCase


class TestChatApp(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_ignore_strings(self):
        app_test = app.test_client(self)
        r = app_test.get('/favicon.ico')
        self.assertEqual(400, r.status_code)

        r = app_test.get('/login')
        self.assertEqual(400, r.status_code)

    def test_no_user_render_login(self):
        app_test = app.test_client(self)
        r = app_test.get('/teste')
        self.assertEqual(200, r.status_code)

    def test_user_render_chat(self):
        app_test = app.test_client(self)
        r = app_test.post('/teste', data={'email': 'email@teste.com.br'})
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed('chat.html')

    def test_user_empty_render_login(self):
        app_test = app.test_client(self)
        r = app_test.post('/teste', data={'email': ''})
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed('login.html')

    def test_user_session_render_chat(self):
        app_test = app.test_client(self)
        r = app_test.post('/teste', data={'email': 'email@teste.com.br'})
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed('chat.html')
        r = app_test.get('/teste')
        self.assertTemplateUsed('chat.html')

    def test_user_post_message(self):
        app_test = app.test_client(self)
        r = app_test.post('/new_message/', data='sample_data')
        self.assertEqual(400, r.status_code)
