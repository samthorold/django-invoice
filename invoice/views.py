from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import (
    DeleteForm, InvoiceForm, InvoiceLineForm, InvoiceSearchForm,
    PaymentForm, PaymentSearchForm, WorkTypeForm, WorkTypeSearchForm
)
from .models import Invoice, InvoiceLine, Payment, WorkType
from contacts.models import Contact


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by('-id')
    # https://stackoverflow.com/questions/4591525/is-it-possible-to-pass-query-parameters-via-djangos-url-template-tag
    payee = request.GET.get('payee')
    if payee:
        invoices = invoices.filter(payee__name__icontains=payee)
    patient = request.GET.get('patient')
    if patient:
        # https://stackoverflow.com/questions/15507171/django-filter-query-foreign-key
        invoices = invoices.filter(invoiceline__patient__name__icontains=patient)
    # if not (payee or patient):
    #     invoices = invoices.all()

    # https://stackoverflow.com/questions/5728283/
    # distinct returns only unique Invoice objects
    # the same Invoice shows up when two+ InvoiceLine objects have a matching patient name
    paginator = Paginator(invoices.distinct(), 15)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    return render(request, 'invoice/invoice_list.html',
        {'invoices': invoices, 'patient': patient, 'payee': payee})

@login_required
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

@login_required
def invoice_search(request):
    if request.method == 'POST':
        form = InvoiceSearchForm(request.POST)
        if form.is_valid():
            payee = form.cleaned_data.get('payee_name')
            patient = form.cleaned_data.get('patient_name')
            url = reverse('invoice:invoice_list')
            url = "{}?payee={}&patient={}".format(url, payee, patient)
            return HttpResponseRedirect(url)
    else:
        form = InvoiceSearchForm()
        return render(request, 'invoice/invoice_search.html', {'form': form})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoice/invoice_detail.html', {'invoice': invoice})

@login_required
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
        return render(request, 'invoice/invoice_edit.html', {'form': form})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def invoice_line_send_invoice_now(request, pk):
    invoice_line = get_object_or_404(InvoiceLine, pk=pk)
    invoice_line.invoice_sent_date = timezone.now()
    invoice_line.save()
    messages.success(request, 'Success, changes were saved :)')
    return redirect('invoice:invoice_detail', pk=invoice_line.invoice.id)

@login_required
def invoice_line_paid_now(request, pk):
    invoice_line = get_object_or_404(InvoiceLine, pk=pk)

    payment = Payment(
        amount=invoice_line.total_fee(),
        date=timezone.now(),
        invoice=invoice_line.invoice
    )

    payment.save()
    messages.success(request, 'Success, changes were saved :)')
    return redirect('invoice:invoice_detail', pk=invoice_line.invoice.id)

@login_required
def worktype_list(request):
    start = request.GET.get('start')
    if not start:
        now = timezone.now()
        year = now.year - 1
        month = now.month
        day = now.day
        start = "{}-{}-{}".format(year, month, day)
    end = request.GET.get('end')
    worktypes = [(w, w.total_fees(start, end)) for w in WorkType.objects.all()]
    # Show all worktypes so they can be edited
    # worktypes = [worktype_tuple for worktype_tuple in worktypes if worktype_tuple[1]>0]
    return render(request, 'invoice/worktype_list.html',
        {'worktypes': worktypes, 'start': start, 'end': end})

@login_required
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

@login_required
def worktype_search(request):
    if request.method == 'POST':
        form = WorkTypeSearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            url = reverse('invoice:worktype_list')
            url = "{}?start={}&end={}".format(url, start, end).replace('None', '')
            return HttpResponseRedirect(url)
    else:
        form = WorkTypeSearchForm()
        return render(request, 'invoice/worktype_search.html', {'form': form})

@login_required
def worktype_detail(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    return render(request, 'invoice/worktype_detail.html', {'worktype': worktype})

@login_required
def worktype_edit(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    if request.method == 'POST':
        form = WorkTypeForm(request.POST, instance=worktype)
        if form.is_valid():
            worktype = form.save()
            messages.success(request, 'Success, changes saved :)')
            return redirect('invoice:worktype_list')
    else:
        form = WorkTypeForm(instance=worktype)
        return render(request, 'invoice/worktype_edit.html', {'form': form})

@login_required
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

@login_required
def payment_list(request):
    """
    Payments by Payee
    """

    start = request.GET.get('start')
    if not start:
        now = timezone.now()
        year = now.year - 1
        month = now.month
        day = now.day
        start = "{}-{}-{}".format(year, month, day)
    end = request.GET.get('end')
    payees = [
        [c, c.total_payments(start, end), c.total_invoiced(start, end), c.total_fees(start, end)]
        for c in Contact.objects.all()
    ]

    payees = [payment_tuple for payment_tuple in payees if
              ((payment_tuple[1]>0) | (payment_tuple[2]>0) | (payment_tuple[3]>0))]

    # "Outstanding" fees
    for payee in payees:
        payee.append(payee[3] - payee[1])

    total_payments = sum(p[1] for p in payees)
    total_invoiced = sum(p[2] for p in payees)
    total_fees = sum(p[3] for p in payees)

    payees = sorted(payees, key=lambda payee: -payee[4])

    return render(
        request, 'invoice/payment_list.html',
        {
            'payees': payees, 'start': start, 'end': end, 'total_payments': total_payments,
            'total_invoiced': total_invoiced, 'total_fees': total_fees
        }
    )

@login_required
def payment_month_list(request):
    now = timezone.now()
    dates = [{'year': now.year, 'month': now.month},]
    for i in range(11):
        if dates[-1]['month'] == 1:
            dates.append({'year': dates[-1]['year']-1, 'month': 12})
        else:
            dates.append({'year': dates[-1]['year'], 'month': dates[-1]['month']-1})

    for i, date in enumerate(dates):
        date['payments'] = sum(
            p.amount for p in Payment.objects.filter(
                date__year=date['year'], date__month=date['month']
            )
        )
        date['invoiced'] = sum(
            il.total_fee() for il in InvoiceLine.objects.filter(
                invoice_sent_date__year=date['year'], invoice_sent_date__month=date['month']
            )
        )
        date['fees'] = sum(
            il.total_fee() for il in InvoiceLine.objects.filter(
                start_date__year=date['year'], start_date__month=date['month']
            )
        )
    total_payments = sum(date['payments'] for date in dates)
    total_invoiced = sum(date['invoiced'] for date in dates)
    total_fees = sum(date['fees'] for date in dates)
    return render(request, 'invoice/payment_month_list.html',
        {'dates': dates, 'total_payments': total_payments, 'total_invoiced':total_invoiced,
         'total_fees': total_fees})


@login_required
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

@login_required
def payment_search(request):
    if request.method == 'POST':
        form = PaymentSearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            url = reverse('invoice:payment_list')
            url = "{}?start={}&end={}".format(url, start, end).replace('None', '')
            return HttpResponseRedirect(url)
    else:
        form = PaymentSearchForm()
        return render(request, 'invoice/payment_search.html', {'form': form})

@login_required
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

@login_required
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
