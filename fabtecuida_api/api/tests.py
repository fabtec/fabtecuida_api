from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import User, Entity, Item, Order

def create_base_data():
	Entity.objects.create(name='clinica santa maria')
	Item.objects.create(name='mascara n95')

def create_test_user():
	User.objects.create_user(username='test', password='test')

def get_test_user_token(client):
	url = reverse('token_obtain_pair')
	data = {"username": "test", "password": "test"}
	return client.post(url, data, format='json')

class AuthTests(APITestCase):

	def setUp(self):
		create_test_user()

	def test_valid_user(self):
		"""
		Ensure user token validation.
		"""
		response = get_test_user_token(self.client)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrdersTests(APITestCase):

	def setUp(self):
		create_test_user()
		create_base_data()

	def test_create_order(self):
		"""
		Ensure we can create a new order.
		"""
		auth_res = get_test_user_token(self.client).json()

		url = reverse('orders')
		data = {'entity': 1}
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_res['access'])
		response = client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Order.objects.count(), 1)
		self.assertEqual(Order.objects.get().entity.id, 1)