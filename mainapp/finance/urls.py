# finance/urls.py

from django.urls import path
from . import views
from .views import TestErrorView
urlpatterns = [
    # ----------------------------
    # Home or Dashboard URL
    # ----------------------------
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('test-error/', TestErrorView.as_view(), name='test-error'),
    # ----------------------------
    # Customer URLs
    # ----------------------------
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(),
         name='customer_create'),
    path('customers/update/<int:pk>/',
         views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/',
         views.CustomerDeleteView.as_view(), name='customer_delete'),

    # ----------------------------
    # Product URLs
    # ----------------------------
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(),
         name='product_create'),
    path('products/update/<int:pk>/',
         views.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/',
         views.ProductDeleteView.as_view(), name='product_delete'),

    # ----------------------------
    # Invoice URLs
    # ----------------------------
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', views.InvoiceCreateView.as_view(),
         name='invoice_create'),
    path('invoices/update/<int:pk>/',
         views.InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/delete/<int:pk>/',
         views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/detail/<int:pk>/',
         views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/pdf/<int:pk>/',
         views.InvoicePDFView.as_view(), name='invoice_pdf'),

    # ----------------------------
    # Expense URLs
    # ----------------------------
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(),
         name='expense_create'),
    path('expenses/update/<int:pk>/',
         views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/delete/<int:pk>/',
         views.ExpenseDeleteView.as_view(), name='expense_delete'),

    # ----------------------------
    # Reporting URLs
    # ----------------------------
    path('reports/sales/', views.SalesReportView.as_view(), name='sales_report'),

    # ----------------------------
    # Home or Dashboard URL
    # ----------------------------
    # You can add a dashboard view if needed
    # path('', views.DashboardView.as_view(), name='dashboard'),
]
