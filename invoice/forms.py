from django import forms

from .models import Invoice, InvoiceLine, Payment, WorkType


class WorkTypeForm(forms.ModelForm):

    class Meta:
        model = WorkType
        fields = ('name',)

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('payee', 'notes')

class InvoiceSearchForm(forms.Form):
    payee_name = forms.CharField(required=False, max_length=200)
    patient_name = forms.CharField(required=False, max_length=200)

class InvoiceLineForm(forms.ModelForm):

    class Meta:
        model = InvoiceLine
        # add the Invoice from the view
        fields = ('patient', 'work_type', 'fee', 'quantity', 'date', 'billable')

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        # add the Invoice from the view
        fields = ('date', 'amount')

class PaymentSearchForm(forms.Form):
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)

class WorkTypeSearchForm(forms.Form):
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)

class DeleteForm(forms.Form):

    entry = forms.CharField()
