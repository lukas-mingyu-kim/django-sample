from django.test import TestCase

from sample_api import models


class SampleApiTests(TestCase):

    def test_login(self):
        response = self.client.post('/api/login', data={"card_num": "1234", "pin_num": 1234})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'user_id')
        self.assertContains(response, 'token')

    def test_accounts(self):
        login_response = self.client.post('/api/login', data={"card_num": "1234", "pin_num": 1234})
        user_id = login_response.data['user_id']
        token = login_response.data['token']

        user = models.AtmUser.objects.get(id=user_id)
        account = models.Account.objects.create(user=user, account_num='test-account-num', balance=5000)
        account.save()

        account_response = self.client.get(f'/api/users/{user_id}/accounts', data={},
                                           **{'HTTP_AUTHORIZATION': f'Token {token}'})
        self.assertEquals(account_response.status_code, 200)
        self.assertContains(account_response, 'accounts')
        self.assertEquals(len(account_response.data['accounts']), 1)
        self.assertEquals(account_response.data['accounts'][0]['account_num'], 'test-account-num')
        self.assertEquals(account_response.data['accounts'][0]['balance'], 5000)

    def test_deposit(self):
        login_response = self.client.post('/api/login', data={"card_num": "1234", "pin_num": 1234})
        user_id = login_response.data['user_id']
        token = login_response.data['token']

        user = models.AtmUser.objects.get(id=user_id)
        account = models.Account.objects.create(user=user, account_num='test-account-num', balance=5000)
        account.save()

        account_response = self.client.post(f'/api/users/{user_id}/deposit',
                                            data={"account_num": "test-account-num", "amount": 300},
                                            **{'HTTP_AUTHORIZATION': f'Token {token}'})
        self.assertEquals(account_response.status_code, 200)
        self.assertContains(account_response, 'account')
        self.assertEquals(account_response.data['account']['account_num'], 'test-account-num')
        self.assertEquals(account_response.data['account']['balance'], 5300)

    def test_withdraw(self):
        login_response = self.client.post('/api/login', data={"card_num": "1234", "pin_num": 1234})
        user_id = login_response.data['user_id']
        token = login_response.data['token']

        user = models.AtmUser.objects.get(id=user_id)
        account = models.Account.objects.create(user=user, account_num='test-account-num', balance=5000)
        account.save()

        account_response = self.client.post(f'/api/users/{user_id}/withdraw',
                                            data={"account_num": "test-account-num", "amount": 300},
                                            **{'HTTP_AUTHORIZATION': f'Token {token}'})
        self.assertEquals(account_response.status_code, 200)
        self.assertContains(account_response, 'account')
        self.assertEquals(account_response.data['account']['account_num'], 'test-account-num')
        self.assertEquals(account_response.data['account']['balance'], 4700)
