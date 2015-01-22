from django.conf import settings
from django.test import TestCase
from context_processors import login_disabled
from django.contrib.auth.models import User
from django.test.client import Client
from django.core import mail
from django.core.mail import mail_admins
import re
from models import UserData, EmailVerification

class ContextProcessorTests(TestCase):
    def test_login_disabled(self):
        result = login_disabled(None)
        
        self.assertTrue('LOGIN_DISABLED' in result)
        self.assertEqual(result['LOGIN_DISABLED'], not settings.DEBUG)


class ForgotPasswordTests(TestCase):
    def setUp(self):
        self.username = 'somedude'
        self.email = 'somedude@example.com'
        self.pw1 = 'a$b$c$d'
        self.pw2 = 'w!x!y!z'
        self.user = User.objects.create_user(self.username, self.email, 
                                             self.pw1)
        UserData.objects.create(user=self.user, email_verified=True)
    
    def testForgotPassword(self):
        """Positive test; Forgot a password, receive a reset email, click on 
        the link in the mail, and choose a new password. 
        """
        
        c = Client()
        
        # make sure we can log in: 
        self.assertTrue(c.login(username=self.username, password=self.pw1))
        c.logout()
        
        r = c.get('/account/forgot/')
        self.assertEqual(r.status_code, 200, 'bad status on forgot')
        
        r = c.post('/account/forgot/', {'email': self.user.email})
        self.assertEqual(r.status_code, 200, 'email addr not accepted')

        self.assertTrue(EmailVerification.objects.filter(user=self.user).exists())

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox.pop()
        self.assertEqual(message.subject, 'MARCO Sign-in Information', 
                         'wrong verify subject line')
        
        # find the reset link (/account/forgot/-hash-)
        match = re.search('http://[^/]+/([/a-z0-9A-Z]+)', message.body)
        self.assertIsNotNone(match.groups(), 'no url in message')
        self.assertEqual(len(match.groups()), 1, 'no url in message')
        url = '/' + match.groups()[0]
        
        # follow the link
        r = c.get(url)
        self.assertEqual(r.status_code, 200, 'bad verify link')
        
        # reset the password
        r = c.post(url, {'password1': self.pw2, 'password2': self.pw2})
        self.assertEqual(r.status_code, 200, 'bad status')
        
        # make sure the EV was deleted
        self.assertFalse(EmailVerification.objects.filter(user=self.user).exists(),
                         'EmailVerification object not deleted')
        
        self.assertFalse(c.login(username=self.username, password=self.pw1), 
                        'passsword not reset')
        c.logout()
        self.assertTrue(c.login(username=self.username, password=self.pw2),
                        'password not reset')
        
    def testResetPasswordFormLoggedIn(self):
        c = Client()
        c.login(username=self.username, password=self.pw1)
        
        resp = c.get('/account/forgot/')
        
        # Trying to remember a password while logged in should get you bounced.
        self.assertTrue(resp.status_code, 301)

    