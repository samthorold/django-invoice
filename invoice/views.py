from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import InvoiceForm, InvoiceLineForm, PaymentForm, WorkTypeForm
from .models import Invoice, InvoiceLine, Payment, WorkType


def invoice_list(request):
	invoices = Invoice.objects.all()
	return render(request, 'invoice/invoice_list.html', {'invoices': invoices})

def invoice_new(request):
	if request.method == 'POST':
		form = InvoiceForm(request.POST)
		if form.is_valid():
			invoice = form.save()
			messages.success(request, 'Success, new invoice created :)')
			return redirect('invoice:invoice_detail', pk=invoice.id)
	else:
		form = InvoiceForm()
		return render(request, 'invoice/invoice_new.html', {'form': form})

def invoice_detail(request, pk):
	invoice = get_object_or_404(Invoice, pk=pk)
	return render(request, 'invoice/invoice_detail.html', {'invoice': invoice})

def invoice_edit(request, pk):
	invoice = get_object_or_404(Invoice, pk=pk)
	if request.method == 'POST':
		form = InvoiceForm(request.POST, instance=invoice)
		if form.is_valid():
			invoice = form.save()
			messages.success(request, 'Success, changes saved :)')
			return redirect('invoice:invoice_detail', pk=invoice.id)
	else:
		form = InvoiceForm(instance=invoice)
		return render(request, 'invoice/invoice_edit.html', {'form', form})

def invoice_delete(request, pk):
	pass

def invoice_line_new(request, invoice_pk):
	pass

def invoice_line_edit(request, pk):
	pass

def invoice_line_delete(request, pk):
	pass

def worktype_list(request):
	pass

def worktype_new(request):
	pass

def worktype_detail(request, pk):
	pass

def worktype_edit(request, pk):
	pass

def worktype_delete(request, pk):
	pass

def payment_list(request):
	pass

def payment_new(request, invoice_pk):
	pass

def payment_edit(request, pk):
	pass

def payment_delete(request, pk):
	pass
