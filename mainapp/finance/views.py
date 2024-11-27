# finance/views.py

import json
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Customer, Product, Invoice, InvoiceItem, Expense
from .forms import (
    CustomerForm,
    ProductForm,
    InvoiceForm,
    InvoiceItemForm,
    ExpenseForm,
)

# Define InvoiceItemFormSet for inline formsets
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True,
)

# ----------------------------
# Customer Views
# ----------------------------


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'finance/customer_list.html'
    context_object_name = 'customers'


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'finance/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'finance/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    template_name = 'finance/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# ----------------------------
# Product Views
# ----------------------------


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'finance/product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'finance/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'finance/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    template_name = 'finance/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# ----------------------------
# Invoice Views
# ----------------------------


class InvoiceListView(LoginRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'finance/invoice_list.html'
    context_object_name = 'invoices'


class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice
    template_name = 'finance/invoice_detail.html'
    context_object_name = 'invoice'


class InvoiceCreateView(LoginRequiredMixin, View):
    template_name = 'finance/invoice_form.html'

    def get(self, request, *args, **kwargs):
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.salesperson = request.user  # Assign the logged-in user as salesperson
            invoice.save()
            formset.instance = invoice
            formset.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoice_list')
        return render(request, self.template_name, {'form': form, 'formset': formset})


class InvoiceUpdateView(LoginRequiredMixin, View):
    template_name = 'finance/invoice_form.html'

    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('invoice_list')
        return render(request, self.template_name, {'form': form, 'formset': formset})


class InvoiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Invoice
    template_name = 'finance/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice_list')

# ----------------------------
# Expense Views
# ----------------------------


class ExpenseListView(LoginRequiredMixin, generic.ListView):
    model = Expense
    template_name = 'finance/expense_list.html'
    context_object_name = 'expenses'


class ExpenseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('expense_list')


class ExpenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('expense_list')


class ExpenseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Expense
    template_name = 'finance/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

# ----------------------------
# PDF Generation Views
# ----------------------------


class InvoicePDFView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        template_path = 'finance/invoice_pdf.html'
        context = {'invoice': invoice}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

# ----------------------------
# Reporting Views
# ----------------------------


class SalesReportView(LoginRequiredMixin, View):
    template_name = 'finance/sales_report.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.filter(status='Paid')
        total_sales = sum(invoice.get_total() for invoice in invoices)
        context = {
            'invoices': invoices,
            'total_sales': total_sales,
        }
        return render(request, self.template_name, context)


# ----------------------------
# Dashboard View
# ----------------------------

class DashboardView(LoginRequiredMixin, View):
    template_name = 'finance/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Sales Over Time Data
        sales_data = (
            Invoice.objects.filter(status='Paid')
            .annotate(month=TruncMonth('date_created'))
            .annotate(
                total_item=ExpressionWrapper(
                    F('items__product__unit_price') * F('items__quantity'),
                    output_field=FloatField()
                )
            )
            .values('month')
            .annotate(total=Sum('total_item'))
            .order_by('month')
        )

        sales_labels = [entry['month'].strftime(
            '%B %Y') for entry in sales_data]
        sales_totals = [float(entry['total']) for entry in sales_data]

        # Expenses by Category Data
        expenses_data = (
            Expense.objects.values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        expense_labels = [entry['category'] for entry in expenses_data]
        expense_totals = [float(entry['total']) for entry in expenses_data]

        # Invoices Status Distribution Data
        status_data = (
            Invoice.objects.annotate(
                total_item=ExpressionWrapper(
                    F('items__product__unit_price') * F('items__quantity'),
                    output_field=FloatField()
                )
            )
            .values('status')
            .annotate(total=Sum('total_item'))
            .order_by('-total')
        )

        status_labels = [entry['status'] for entry in status_data]
        status_totals = [float(entry['total']) for entry in status_data]

        # Top Customers Data
        top_customers = (
            Invoice.objects.filter(status='Paid')
            .annotate(
                total_item=ExpressionWrapper(
                    F('items__product__unit_price') * F('items__quantity'),
                    output_field=FloatField()
                )
            )
            .values('customer__name')
            .annotate(total=Sum('total_item'))
            .order_by('-total')[:5]  # Top 5 customers
        )

        top_customer_labels = [entry['customer__name']
                               for entry in top_customers]
        top_customer_totals = [float(entry['total'])
                               for entry in top_customers]

        context = {
            'sales_labels': json.dumps(sales_labels),
            'sales_totals': json.dumps(sales_totals),
            'expense_labels': json.dumps(expense_labels),
            'expense_totals': json.dumps(expense_totals),
            'status_labels': json.dumps(status_labels),
            'status_totals': json.dumps(status_totals),
            'top_customer_labels': json.dumps(top_customer_labels),
            'top_customer_totals': json.dumps(top_customer_totals),
        }
        return render(request, self.template_name, context)
