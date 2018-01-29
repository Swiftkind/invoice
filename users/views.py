from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from users.forms import *
from users.models import User



class SigninView(TemplateView):
    template_name = 'users/signin.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        form = SigninForm()
        return render(self.request, self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = SigninForm(self.request.POST)
        if form.is_valid():
            #import pdb; pdb.set_trace()
        
            login(self.request, form.auth)
            messages.error(request, 'Welcome Home')
            return redirect('index')
        else:
            context={
                'form':form,
            }
        return render(self.request, self.template_name, context)



class SignupView(TemplateView):
    template_name = 'users/signup.html'

    def get(self, *args, **kwargs):
        form = SignupForm()
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        try:
            auth = self.request.user
            form = SignupForm(self.request.POST, self.request.FILES, user=auth)
        except:
            auth = ''
            form = SignupForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            user= form.save()
            messages.error(self.request, 'Account successfully created. Activate your account from the admin.')
            return redirect('index')
        return render(self.request, self.template_name, {'form': form})



class SignoutView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('signin')



class UserProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'users/profile.html'

    def get(self, *args, **kwargs):
        context = {
                    'user': get_object_or_404(User, pk=kwargs['user_id'])
                  }
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass



class UserUpdateView(LoginRequiredMixin,TemplateView):
    template_name = 'users/update_user.html'

    def get(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        context = {
                    'form': UserUpdateForm(instance=user)
                  }
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        form = UserUpdateForm(self.request.POST, self.request.FILES,instance=user)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'User is successfully updated')
            return redirect('index' )
        else:
            print("invalid")
            context = {
                'form' : form,
                }
        return render(self.request, self.template_name, context=context)



class SubUsersView(LoginRequiredMixin,TemplateView):
    template_name = 'users/company_users.html'


class SubUserAddView(LoginRequiredMixin,TemplateView):
    template_name = 'users/signup-subuser.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, context=self.get_context_data(**kwargs))

    def post(self,  *args, **kwargs):
        try:
            auth = self.request.user
            logo = self.request.user.logo
            form = SignupForm(self.request.POST, self.request.FILES, user=auth,logo=logo)
        except:
            auth = ''
            form = SignupForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            form.save(commit=False)
            messages.success(self.request, 'Subuser is successfully created')
            return redirect('index')
        else:
            context=self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context=context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs['user_id'])

        form = SignupForm(instance=user)
        context['form'] = form
        context['form_errors'] = form.errors
        return context

class SubUserDeleteView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        pass


