from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q


from clients.models import Client
from clients.forms import  ClientForm
from invoices.models import Invoice


from io import BytesIO
import time



class ClientListView(LoginRequiredMixin,TemplateView):
    '''display list of clients under by company
    '''
    template_name = 'clients/all_client.html'


    def get_context_data(self,**kwargs):
        '''getting the clients data from database
        '''
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            clients = clients.filter(Q(display_name__icontains=query,  company=self.request.user.company) )
        context['clients'] =  clients
        return context


    def get(self, *args, **kwargs):
        '''displaying the data of clients
        '''
        return render(self.request, self.template_name, self.get_context_data(**kwargs))



class ClientView(LoginRequiredMixin,TemplateView):
    '''display client information
    '''
    template_name = 'clients/view_client.html'


    def get_context_data(self,**kwargs):
        '''getting the client data from database
        '''
        context = super().get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, id=kwargs['client_id'])
        context['current_path'] = self.request.path
        context['invoices'] = Invoice.objects.filter(client=kwargs['client_id'])
        return context

    
    def get(self, *args, **kwargs):
        '''displaying the data of client
        '''
        return render(self.request, self.template_name, context=self.get_context_data(**kwargs))



class ClientAddView(LoginRequiredMixin,TemplateView):
    '''Viewing for adding client
    '''
    template_name = 'clients/update_client.html'


    def get(self, *args, **kwargs):
        '''display the client form
        '''
        return render(self.request, self.template_name, context=self.get_context_data(**kwargs))


    def post(self, *args, **kwargs):
        '''getting the filled form of client
        '''
        errors = {}
        form = ClientForm(self.request.POST, user=self.request.user)  
        if form.is_valid():
            '''form validation for client
            '''
            client = form.save(commit=False, company=self.request.user.company)     
            client.save()
            messages.success(self.request, 'Client is successfully added')
            return redirect('clients')
        else:
            context=self.get_context_data(**kwargs)
            context['form'] = form
            context['form_errors'] = form.errors
            return render(self.request, self.template_name, context=context)


    def get_context_data(self,**kwargs):
        '''getting the form for client
        '''
        context = super().get_context_data(**kwargs)
        context['form'] = ClientForm() 
        return context



class ClientEditView(LoginRequiredMixin,TemplateView):
    '''View edit form client
    '''
    template_name = 'clients/update_client.html'


    def get(self, *args, **kwargs):
        '''display the client form
        '''
        return render(self.request, self.template_name, context=self.get_context_data(**kwargs))


    def post(self, request, *args, **kwargs):
        '''getting the filled client form
        '''
        client = get_object_or_404(Client, id=kwargs['client_id'])
        form = ClientForm(self.request.POST, user=self.request.user, instance=client)
        
        if form.is_valid():
            '''form validdation for editing client
            '''
            client = form.save(commit=False, company=self.request.user.company)
            client.save()
            messages.success(request, 'Client is successfully updated')
            return redirect('clients')
        else:
            context=self.get_context_data(**kwargs)
            context['form'] = form
            context['form_errors'] = form.errors
            return render(self.request, self.template_name, context=context)


    def get_context_data(self,**kwargs):
        '''getting the instance form of client
        '''
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, id=kwargs['client_id'])
        context['form'] = ClientForm(instance=client)
        return context



class ClientDeleteView(LoginRequiredMixin,View):
    '''view for deleting client
    '''

    def get(self, request, *args, **kwargs):
        '''get the client
        '''
        client = get_object_or_404(Client, id=kwargs['client_id'])
        client.delete()
        messages.error(request, 'Client is successfully deleted')
        return redirect('clients')