from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from contacts.models import (
								Contact, 
								AddMoreField,
								BillingAddress, 
								ShippingAddress,
								ContactPerson
							)

from contacts.forms import  (
								ContactForm, 
								AddMoreFieldForm,
								#OtherDetailForm,
								BillingAddressForm, 
								ShippingAddressForm, 
								AdditionalAddressForm,
								ContactPersonForm
							)


contact_info = {
					'contact_form': ContactForm(prefix='contact'),
					#'add_more_field_form': AddMoreFieldForm(prefix='add-more-field'),
					#'other_detail_form': OtherDetailForm(),
					'billing_address_form': BillingAddressForm(prefix='billing'),
					'shipping_address_form': ShippingAddressForm(prefix='shipping'),
					'additional_address_form': AdditionalAddressForm(prefix='additional'),
					'contact_person_form': ContactPersonForm(prefix='contact-person')
				}



# Create your views here.
@method_decorator(login_required, name='dispatch')
class ContactsView(TemplateView):
	template_name = 'contacts/all_contact.html'

	def get(self, request, *args, **kwargs):
		return render(self.request, self.template_name, {'contacts': Contact.objects.all()})


@method_decorator(login_required, name='dispatch')
class ContactViewView(TemplateView):
	template_name = 'contacts/view_contact.html'

	def get(self, request, *args, **kwargs):
		contact = get_object_or_404(Contact, id=kwargs['contact_id'])
		return render(self.request, self.template_name, {'contact': contact})



class ContactAddView(TemplateView):
	template_name = 'contacts/add_contact.html'

	def get(self, request, *args, **kwargs):
		context = contact_info
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		contact_form            = ContactForm(self.request.POST, prefix='contact')
		#add_more_field_form     = AddMoreFieldForm(self.request.POST, prefix='add-more-field')
		#other_detail_form       = OtherDetailForm(self.request.POST)
		billing_address_form    = BillingAddressForm(self.request.POST, prefix='billing')
		shipping_address_form   = ShippingAddressForm(self.request.POST, prefix='shipping')
		additional_address_form = AdditionalAddressForm(self.request.POST, prefix='additional')
		contact_person_form     = ContactPersonForm(self.request.POST, prefix='contact-person')

		contact          = Contact()
		billing_address  = BillingAddress()
		shipping_address = ShippingAddress()
		contact_person   = ContactPerson() 
		
		if (     contact_form.is_valid()
			 and billing_address_form.is_valid()
			 and shipping_address_form.is_valid()
			 and additional_address_form.is_valid()
			 and contact_person_form.is_valid() ):
		
			contact.salutation           = contact_form.cleaned_data['salutation']
			contact.first_name           = contact_form.cleaned_data['first_name']
			contact.last_name            = contact_form.cleaned_data['last_name']
			contact.email_address        = contact_form.cleaned_data['email_address']
			contact.work_phone           = contact_form.cleaned_data['work_phone']
			contact.mobile               = contact_form.cleaned_data['mobile']
			contact.contact_display_name = contact_form.cleaned_data['contact_display_name']
			contact.company_name         = contact_form.cleaned_data['company_name']
			contact.website              = contact_form.cleaned_data['website']

			contact.currency             = contact_form.cleaned_data['currency']
			contact.payment_terms        = contact_form.cleaned_data['payment_terms']
			contact.portal               = contact_form.cleaned_data['portal']
			contact.portal_language      = contact_form.cleaned_data['portal_language']
			contact.facebook             = contact_form.cleaned_data['facebook']
			contact.twitter              = contact_form.cleaned_data['twitter']
			contact.remarks              = contact_form.cleaned_data['remarks']

			#contact.add_more_field.skype_account = add_more_field_form.cleaned_data['skype_account']
			#contact.add_more_field.designation   = add_more_field_form.cleaned_data['designation']
			#contact.add_more_field.department    = add_more_field_form.cleaned_data['department']

			
			billing_address.attention = billing_address_form.cleaned_data['attention']
			billing_address.street_1  = billing_address_form.cleaned_data['street_1']
			billing_address.street_2  = billing_address_form.cleaned_data['street_2']
			billing_address.city      = billing_address_form.cleaned_data['city']
			billing_address.state     = billing_address_form.cleaned_data['state']
			billing_address.zip_code  = billing_address_form.cleaned_data['zip_code']
			billing_address.country   = billing_address_form.cleaned_data['country']
			billing_address.phone     = billing_address_form.cleaned_data['phone']
			billing_address.fax       = billing_address_form.cleaned_data['fax']

			
			shipping_address.attention = shipping_address_form.cleaned_data['attention']
			shipping_address.street_1  = shipping_address_form.cleaned_data['street_1']
			shipping_address.street_2  = shipping_address_form.cleaned_data['street_2']
			shipping_address.city      = shipping_address_form.cleaned_data['city']
			shipping_address.state     = shipping_address_form.cleaned_data['state']
			shipping_address.zip_code  = shipping_address_form.cleaned_data['zip_code']
			shipping_address.country   = shipping_address_form.cleaned_data['country']
			shipping_address.phone     = shipping_address_form.cleaned_data['phone']
			shipping_address.fax       = shipping_address_form.cleaned_data['fax']

			contact_person.salutation    = contact_person_form.cleaned_data['salutation']
			contact_person.first_name    = contact_person_form.cleaned_data['first_name']
			contact_person.last_name     = contact_person_form.cleaned_data['last_name']
			contact_person.email_address = contact_person_form.cleaned_data['email_address']
			contact_person.work_phone    = contact_person_form.cleaned_data['work_phone']
			contact_person.mobile        = contact_person_form.cleaned_data['mobile']
			
			billing_address.save()
			shipping_address.save()
			contact_person.save()
			contact.billing_address  = billing_address
			contact.shipping_address = shipping_address
			contact.contact_person   = contact_person
			contact.save()

			return redirect('contacts')
		else:
			context = contact_info
		return render(self.request, self.template_name, context)


class ContactEditView(TemplateView):
	template_name = 'contacts/edit_contact.html'

	def get(self, request, *args, **kwargs):
		contact = get_object_or_404(Contact, id=kwargs['contact_id'])
		context = {
							'contact_form': ContactForm(instance=contact, prefix='contact'),
							'billing_address_form': BillingAddressForm(instance=contact.billing_address, prefix='billing'),
							'shipping_address_form': ShippingAddressForm(instance=contact.shipping_address, prefix='shipping'),
							'contact_person_form': ContactPersonForm(instance=contact.contact_person, prefix='contact-person')
				  }
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		contact = get_object_or_404(Contact, id=kwargs['contact_id'])
		billing_address  = get_object_or_404(BillingAddress, id=contact.billing_address.id)
		shipping_address = get_object_or_404(ShippingAddress, id=contact.shipping_address.id)
		contact_person = get_object_or_404(ContactPerson, id=contact.contact_person.id)
				
		contact_form            = ContactForm(self.request.POST,prefix='contact', instance=contact)
		#add_more_field_form     = AddMoreFieldForm(self.request.POST, prefix='add-more-field')
		#other_detail_form       = OtherDetailForm(self.request.POST)
		billing_address_form    = BillingAddressForm(self.request.POST,instance=contact.billing_address, prefix='billing')
		shipping_address_form   = ShippingAddressForm(self.request.POST,instance=contact.shipping_address, prefix='shipping')
		additional_address_form = AdditionalAddressForm(self.request.POST,instance=contact.additional_address, prefix='additional')
		contact_person_form     = ContactPersonForm(self.request.POST,instance=contact.contact_person, prefix='contact-person')
		
		if (     contact_form.is_valid()
			 and billing_address_form.is_valid()
			 and shipping_address_form.is_valid()
			 and additional_address_form.is_valid()
			 and contact_person_form.is_valid() ):
		
			contact.salutation           = contact_form.cleaned_data['salutation']
			contact.first_name           = contact_form.cleaned_data['first_name']
			contact.last_name            = contact_form.cleaned_data['last_name']
			contact.email_address        = contact_form.cleaned_data['email_address']
			contact.work_phone           = contact_form.cleaned_data['work_phone']
			contact.mobile               = contact_form.cleaned_data['mobile']
			contact.contact_display_name = contact_form.cleaned_data['contact_display_name']
			contact.company_name         = contact_form.cleaned_data['company_name']
			contact.website              = contact_form.cleaned_data['website']

			contact.currency             = contact_form.cleaned_data['currency']
			contact.payment_terms        = contact_form.cleaned_data['payment_terms']
			contact.portal               = contact_form.cleaned_data['portal']
			contact.portal_language      = contact_form.cleaned_data['portal_language']
			contact.facebook             = contact_form.cleaned_data['facebook']
			contact.twitter              = contact_form.cleaned_data['twitter']
			contact.remarks              = contact_form.cleaned_data['remarks']

			#contact.add_more_field.skype_account = add_more_field_form.cleaned_data['skype_account']
			#contact.add_more_field.designation   = add_more_field_form.cleaned_data['designation']
			#contact.add_more_field.department    = add_more_field_form.cleaned_data['department']

			
			billing_address.attention = billing_address_form.cleaned_data['attention']
			billing_address.street_1  = billing_address_form.cleaned_data['street_1']
			billing_address.street_2  = billing_address_form.cleaned_data['street_2']
			billing_address.city      = billing_address_form.cleaned_data['city']
			billing_address.state     = billing_address_form.cleaned_data['state']
			billing_address.zip_code  = billing_address_form.cleaned_data['zip_code']
			billing_address.country   = billing_address_form.cleaned_data['country']
			billing_address.phone     = billing_address_form.cleaned_data['phone']
			billing_address.fax       = billing_address_form.cleaned_data['fax']

			
			shipping_address.attention = shipping_address_form.cleaned_data['attention']
			shipping_address.street_1  = shipping_address_form.cleaned_data['street_1']
			shipping_address.street_2  = shipping_address_form.cleaned_data['street_2']
			shipping_address.city      = shipping_address_form.cleaned_data['city']
			shipping_address.state     = shipping_address_form.cleaned_data['state']
			shipping_address.zip_code  = shipping_address_form.cleaned_data['zip_code']
			shipping_address.country   = shipping_address_form.cleaned_data['country']
			shipping_address.phone     = shipping_address_form.cleaned_data['phone']
			shipping_address.fax       = shipping_address_form.cleaned_data['fax']

			contact_person.salutation    = contact_person_form.cleaned_data['salutation']
			contact_person.first_name    = contact_person_form.cleaned_data['first_name']
			contact_person.last_name     = contact_person_form.cleaned_data['last_name']
			contact_person.email_address = contact_person_form.cleaned_data['email_address']
			contact_person.work_phone    = contact_person_form.cleaned_data['work_phone']
			contact_person.mobile        = contact_person_form.cleaned_data['mobile']
			
			billing_address.save()
			shipping_address.save()
			contact_person.save()
			contact.billing_address  = billing_address
			contact.shipping_address = shipping_address
			contact.contact_person   = contact_person
			contact.save()

			return redirect('contacts')
		else:
			context = {
							'contact_form': ContactForm(instance=contact, prefix='contact'),
							'billing_address_form': BillingAddressForm(instance=contact.billing_address, prefix='billing'),
							'shipping_address_form': ShippingAddressForm(instance=contact.shipping_address, prefix='shipping'),
							'contact_person_form': ContactPersonForm(instance=contact.contact_person, prefix='contact-person')
						}
		return render(self.request, self.template_name, context)



class ContactDeleteView(TemplateView):
	def get(self, request, *args, **kwargs):
		contact = get_object_or_404(Contact, id=kwargs['contact_id'])
		contact.delete()
		return redirect('contacts')