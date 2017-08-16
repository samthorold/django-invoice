from django import forms

from .models import Invoice, InvoiceLine, Payment, WorkType


class WorkTypeForm(forms.ModelForm):

    class Meta:
        model = WorkType
        fields = ('name',)

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('payee',)

class InvoiceLineForm(forms.ModelForm):

    class Meta:
        model = InvoiceLine
        # add the Invoice from the view
        fields = ('patient', 'work_type', 'fee', 'quantity', 'billable')

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        # add the Invoice from the view
        fields = ('date', 'amount')
