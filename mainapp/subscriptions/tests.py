from django.test import TestCase
from django.urls import reverse
from .models import Subscription


class SubscriptionTests(TestCase):

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(email='test@example.com')
        self.assertEqual(subscription.email, 'test@example.com')

    def test_subscription_list_view(self):
        response = self.client.get(reverse('subscription_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subscriptions')
