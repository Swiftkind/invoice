import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View


from clients.models import Client
from clients.forms import  ClientForm
from clients.mixins import UserIsOwnerMixin
from invoices.models import Invoice
from io import BytesIO



class ClientListView(LoginRequiredMixin,TemplateView):
    """ Display list of clients under by company
    """
    template_name = 'clients/all_client.html'

    def get(self, *args, **kwargs):
        """displaying the data of clients
        """
        context = {}
        clients = Client.objects.filter(company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            clients = clients.filter(display_name__icontains=query)
        context['clients'] =  clients
        return render(self.request, self.template_name, context)



class ClientView(UserIsOwnerMixin,TemplateView):
    """ Display client information
    """
    template_name = 'clients/view_client.html'

    def get(self, *args, **kwargs):
        """ Displaying the data of client
        """
        context = {}
        context['client'] = get_object_or_404(Client, id=kwargs['client_id'])
        context['invoices'] = Invoice.objects.filter(client=kwargs['client_id'])
        return render(self.request, self.template_name, context)



class ClientAddView(LoginRequiredMixin,TemplateView):
    """Viewing for adding client
    """
    template_name = 'clients/add_client.html'

    def get(self, *args, **kwargs):
        """ Display the client form
        """
        context = {}
        context['form'] = ClientForm() 
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """ Getting the filled form of client
        """
        form = ClientForm(self.request.POST, company=self.request.user.company)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = self.request.user
            client.company = self.request.user.company
            client.save()
            messages.success(self.request, 'Client is successfully added')
            return redirect('clients')
        else:
            context = {}
            context['form'] = form
            return render(self.request, self.template_name, context=context)



class ClientEditView(UserIsOwnerMixin,TemplateView):
    """ View edit form client
    """
    template_name = 'clients/update_client.html'

    def get(self, *args, **kwargs):
        """ Display the client form
        """
        context = {}
        client = get_object_or_404(Client, id=kwargs['client_id'])
        context['form'] = ClientForm(instance=client)
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """ Getting the filled client form
        """
        client = get_object_or_404(Client, id=kwargs['client_id'])
        form = ClientForm(self.request.POST,instance=client, company=self.request.user.company)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = self.request.user
            if self.request.user.company:
                client.company = self.request.user.company
            client.save()
            messages.success(request, 'Client is successfully updated')
            return redirect('clients')
        else:
            context = {}
            context['form'] = form
            return render(self.request, self.template_name, context=context)



class ClientDeleteView(UserIsOwnerMixin,View):
    """ View for deleting client
    """
    def get(self, request, *args, **kwargs):
        """ Get the client
        """
        client = get_object_or_404(Client, id=kwargs['client_id'])
        client.delete()
        messages.success(request, 'Client is successfully deleted')
        return redirect('clients')
