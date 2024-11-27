from django.urls import path

from .views import (
    SubscriptionListView,
    SubscriptionCreateView,
    SubscriptionUpdateView,
    SubscriptionDeleteView,
    SubscriptionPDFView,
)

urlpatterns = [
    path('', SubscriptionListView.as_view(), name='subscription_list'),
    path('create/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('update/<int:pk>/', SubscriptionUpdateView.as_view(),
         name='subscription_update'),
    path('delete/<int:pk>/', SubscriptionDeleteView.as_view(),
         name='subscription_delete'),
    path('pdf/<int:pk>/', SubscriptionPDFView.as_view(), name='subscription_pdf'),
]
