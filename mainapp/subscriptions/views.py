from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Subscription
from .forms import SubscriptionForm
from django.http import JsonResponse
from django.shortcuts import redirect
from xhtml2pdf import pisa
from io import BytesIO


class SubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = Subscription
    paginate_by = 10
    template_name = 'subscriptions/subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Subscription.objects.filter(email__icontains=query)
        return Subscription.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class SubscriptionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'subscriptions/subscription_form.html'
    success_url = reverse_lazy('subscription_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription created successfully.')
        return super().form_valid(form)


class SubscriptionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'subscriptions/subscription_form.html'
    success_url = reverse_lazy('subscription_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription updated successfully.')
        return super().form_valid(form)


class SubscriptionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Subscription
    template_name = 'subscriptions/subscription_confirm_delete.html'
    success_url = reverse_lazy('subscription_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            return JsonResponse({'success': True})
        else:
            return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subscription deleted successfully.')
        return super().delete(request, *args, **kwargs)


class SubscriptionPDFView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        subscription = Subscription.objects.get(pk=pk)
        template_path = 'subscriptions/subscription_pdf.html'
        context = {'subscription': subscription}

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="subscription_{subscription.pk}.pdf"'

        # Find the template and render it
        template = get_template(template_path)
        html = template.render(context)

        # Create a PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response)

        # If error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
