from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, ContactSearchForm
from .models import Contact


@login_required
def new_contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			contact = form.save()
			messages.success(request, "Created")
			return redirect('contacts:view_contact', id=contact.id)
	else:
		form = ContactForm()
		return render(request, 'contacts/new_contact.html', {'form': form})

@login_required
def list_contacts(request):
	contacts = Contact.objects.all()
	name = request.GET.get('name')
	if name:
		contacts = contacts.filter(name__icontains=name)

	paginator = Paginator(contacts, 25)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	return render(request, 'contacts/list_contacts.html',
		{'contacts': contacts, 'name': name})

@login_required
def view_contact(request, id):
	contact = get_object_or_404(Contact, pk=id)
	return render(request, 'contacts/view_contact.html', {'contact': contact})

@login_required
def contact_search(request):
	if request.method == 'POST':
		form = ContactSearchForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			url = reverse('contacts:list_contacts')
			url = "{}?name={}".format(url, name)
			return HttpResponseRedirect(url)
	else:
		form = ContactSearchForm()
		return render(request, 'contacts/contact_search.html', {'form': form})

@login_required
def edit_contact(request, id):
	contact = get_object_or_404(Contact, id=id)
	if request.method == 'POST':
		form = ContactForm(request.POST, instance=contact)
		if form.is_valid():
			contact = form.save()
			messages.success(request, "Changes saved")
			return redirect('contacts:view_contact', id=contact.id)
	else:
		form = ContactForm(instance=contact)
		return render(request, 'contacts/edit_contact.html', {'form': form})

@login_required
def delete_contact(request, id):
	contact = get_object_or_404(Contact, id=id)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			if name == contact.name:
				messages.info(request, '"{}" deleted'.format(name))
				contact.delete()
				return redirect('contacts:list_contacts')
			else:
				msg = '"{}" does not match "{}"'.format(name, contact.name)
				messages.warning(request, msg)
				return redirect('contacts:delete_contact', id=id)
	else:
		form = ContactForm()
		return render(request, 'contacts/delete_contact.html',
			{'form': form, 'contact': contact})
