from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import DeleteForm, InvoiceForm, InvoiceLineForm, PaymentForm, WorkTypeForm
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
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data.get('entry')
            if entry == invoice.payee.name:
                invoice.delete()
                messages.success(request, 'Success, invoice deleted :)')
                return redirect('invoice:invoice_list')
            else:
                msg = "{} does not match {}".format(entry, invoice.payee.name)
                messages.warning(request, msg)
                return redirect('invoice:invoice_delete', pk=invoice.id)
    else:
        form = DeleteForm()
        return render(request, 'invoice/invoice_delete.html',
            {'form': form, 'invoice': invoice})

def invoice_line_new(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = InvoiceLineForm(request.POST)
        if form.is_valid():
            # no Invoice yet so commit=False to avoid missing relationship
            invoice_line = form.save(commit=False)
            invoice_line.invoice = invoice
            invoice_line.save()
            messages.success(request, 'Success, invoice line created :)')
            return redirect('invoice:invoice_detail', pk=invoice.id)
    else:
        form = InvoiceLineForm()
        return render(request, 'invoice/invoice_line_new.html', {'form': form})

def invoice_line_edit(request, pk):
    invoice_line = get_object_or_404(InvoiceLine, pk=pk)
    if request.method == 'POST':
        form = InvoiceLineForm(request.POST, instance=invoice_line)
        if form.is_valid():
            invoice_line = form.save()
            messages.success(request, 'Success, changes saved :)')
            return redirect('invoice:invoice_detail', pk=invoice_line.invoice.id)
    else:
        form = InvoiceLineForm(instance=invoice_line)
        return render(request, 'invoice/invoice_line_edit.html', {'form': form})


def invoice_line_delete(request, pk):
    invoice_line = get_object_or_404(InvoiceLine, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data.get('entry')
            if entry == invoice_line.invoice.payee.name:
                invoice_line.delete()
                messages.success(request, 'Success, invoice line deleted :)')
                return redirect('invoice:invoice_detail', pk=invoice_line.invoice.pk)
            else:
                msg = "{} does not match {}".format(entry, invoice_line.invoice.payee.name)
                messages.warning(request, msg)
                return redirect('invoice:invoice_line_delete', pk=invoice_line.id)
    else:
        form = DeleteForm()
        return render(request, 'invoice/invoice_line_delete.html',
            {'form': form, 'invoice_line': invoice_line})

def worktype_list(request):
    worktypes = WorkType.objects.all()
    return render(request, 'invoice/worktype_list.html', {'worktypes': worktypes})

def worktype_new(request):
    if request.method == 'POST':
        form = WorkTypeForm(request.POST)
        if form.is_valid():
            worktype = form.save()
            messages.success(request, 'Success, work type created :)')
            return redirect('invoice:worktype_list')
    else:
        form = WorkTypeForm()
        return render(request, 'invoice/worktype_new.html', {'form': form})

def worktype_detail(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    return render(request, 'invoice/worktype_detail.html', {'worktype': worktype})

def worktype_edit(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    if request.method == 'POST':
        form = WorkTypeForm(request.POST, instance=worktype)
        if form.is_valid():
            worktype = form.save()
            messages.success(request, 'Success, changes saved :)')
            return redirect('invoice:worktype_list')

def worktype_delete(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data.get('entry')
            if entry == worktype.name:
                worktype.delete()
                messages.success(request, 'Success, worktype deleted :)')
                return redirect('invoice:worktype_list')
            else:
                msg = "{} does not match {}".format(entry, worktype.name)
                messages.warning(request, msg)
                return redirect('invoice:worktype_delete', pk=worktype.id)
    else:
        form = DeleteForm()
        return render(request, 'invoice/worktype_delete.html',
            {'form': form, 'worktype': worktype})

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'invoice/payment_list.html', {'payments': payments})

def payment_new(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # no Invoice yet so commit=False to avoid missing relationship
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            messages.success(request, 'Success, payment created :)')
            return redirect('invoice:invoice_detail', pk=invoice.id)
    else:
        form = PaymentForm()
        return render(request, 'invoice/payment_new.html', {'form': form})


def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            messages.success(request, 'Success, changes saved :)')
            return redirect('invoice:invoice_detail', pk=payment.invoice.id)
    else:
        form = PaymentForm(instance=payment)
        return render(request, 'invoice/payment_edit.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data.get('entry')
            if entry == payment.invoice.payee.name:
                payment.delete()
                messages.success(request, 'Success, payment deleted :)')
                return redirect('invoice:invoice_detail', pk=payment.invoice.pk)
            else:
                msg = "{} does not match {}".format(entry, payment.invoice.payee.name)
                messages.warning(request, msg)
                return redirect('invoice:payment_delete', pk=payment.id)
    else:
        form = DeleteForm()
        return render(request, 'invoice/payment_delete.html',
            {'form': form, 'payment': payment})
