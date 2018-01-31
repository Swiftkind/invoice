from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from users.forms import SignupForm, CompanyForm,  SigninForm, UserUpdateForm, SubUserAddForm
from users.models import User, Company



class SigninView(TemplateView):
    """Signin user
    """
    template_name = 'users/signin.html'

    def get(self, *args, **kwargs):
        """Get signin form
        """
        if self.request.user.is_authenticated:
            return redirect('index')
        form = SigninForm()
        return render(self.request, self.template_name,{'form':form})


    def post(self, request, *args, **kwargs):
        """Signin user
        """
        form = SigninForm(self.request.POST)
        if form.is_valid():
            login(self.request, form.auth)
            messages.error(request, 'Welcome Home')
            return redirect('index')
        else:
            context={ 'form':form,}
        return render(self.request, self.template_name, context)



class SignupView(TemplateView):
    """Signup user
    """
    template_name = 'users/signup.html'


    def get(self, *args, **kwargs):
        """Display signup form
        """
        context = { 'signup_form' : SignupForm(),
                    'company_form' : CompanyForm(), }
        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        """Signup a user
        """
        company_form = CompanyForm(self.request.POST, self.request.FILES)
        signup_form = SignupForm(self.request.POST, self.request.FILES)
        
        if signup_form.is_valid() and company_form.is_valid():
            company = company_form.save(commit=False)
            user = signup_form.save(commit=False)
            company.owner = user
            company.save()
            user.company = company
            user.save()  
            messages.error(self.request, 'Account successfully created. Activate your account from the admin.')
            return redirect('index')
        else:
             context = {  'signup_form' : SignupForm(self.request.POST, self.request.FILES),
                          'company_form' : CompanyForm(self.request.POST, self.request.FILES),
                       }
        return render(self.request, self.template_name, context)



class SignoutView(LoginRequiredMixin,View):
    """Signout a user
    """
    def get(self, *args, **kwargs):
        """Logout user and redirect to signin
        """
        logout(self.request)
        return redirect('signin')



class UserProfileView(LoginRequiredMixin,TemplateView):
    """User profile
    """
    template_name = 'users/profile.html'


    def get(self, *args, **kwargs):
        """View user details
        """
        context = { 'user': get_object_or_404(User, pk=kwargs['user_id']) }
        return render(self.request, self.template_name, context=context)



class UserUpdateView(LoginRequiredMixin,TemplateView):
    """Update User
    """
    template_name = 'users/update_user.html'


    def get(self, *args, **kwargs):
        """Display form
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        context = { 'form': UserUpdateForm(instance=user) }
        return render(self.request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        """Update a user
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        form = UserUpdateForm(self.request.POST, self.request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User is successfully updated')
            return redirect('index' )
        else:
            context = { 'form' : form, }
        return render(self.request, self.template_name, context=context)



class SubUserView(LoginRequiredMixin,TemplateView):
    """Subuser details
    """
    template_name = 'users/company_users.html'


    def get(self, *args, **kwargs):
        """Display form
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        context = { 'form': UserUpdateForm(instance=user) }
        return render(self.request, self.template_name, context=context)



class SubUserAddView(LoginRequiredMixin,TemplateView):
    """Add subuser
    """
    template_name = 'users/signup-subuser.html'


    def get(self, *args, **kwargs):
        """Display form
        """
        return render(self.request, self.template_name, context=self.get_context_data(**kwargs))


    def post(self,  *args, **kwargs):
        """Create subuser
        """
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
        """Get form
        """
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs['user_id'])
        form = SignupForm(instance=user)
        context['form'] = form
        context['form_errors'] = form.errors
        return context



