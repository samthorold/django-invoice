from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_date

from contacts.models import Contact


class WorkType(models.Model):

	class Meta:
		ordering = ('name',)

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def total_fees(self, start=None, end=None):
		fees = self.invoiceline_set
		# if start:
		# 	fees = fees.filter(date__gte=start)
		# if end:
		# 	fees = fees.filter(date__lte=end)
		return sum(il.total_fee(start, end, billable=False) for il in fees.all())

class Invoice(models.Model):

	payee = models.ForeignKey('contacts.Contact')
	notes = models.TextField(blank=True)

	def __str__(self):
		return self.payee.name

	@property
	def patients(self):
		return Contact.objects.filter(invoiceline__invoice=self).distinct()

	@property
	def patients_string(self):
		return ", ".join(str(p) for p in self.patients)

	def total_fee(self, start=None, end=None):
		return sum(il.total_fee(start, end) for il in self.invoiceline_set.all())

	def total_payment(self, start=None, end=None):
		payments = self.payment_set
		if start:
			payments = payments.filter(date__gte=start)
		if end:
			payments = payments.filter(date__lte=end)
		return sum(p.amount for p in payments.all())

	def total_invoiced(self, start=None, end=None):
		return sum(il.total_invoiced(start, end) for il in self.invoiceline_set.all())

	def fee_outstanding(self):
		return self.total_fee() - self.total_payment()

class InvoiceLine(models.Model):

	class Meta:
		ordering = ('-billable', 'start_date', 'work_type')

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	work_type = models.ForeignKey(WorkType)
	patient = models.ForeignKey('contacts.Contact')
	quantity = models.IntegerField()
	fee = models.IntegerField()
	start_date = models.DateField(default=timezone.now)
	billable = models.BooleanField(default=True)
	invoice_sent_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return "{}: {}".format(self.work_type.name, self.patient.name)

	def total_fee(self, start=None, end=None, billable=True):
		if billable and not self.billable:
			return 0
		if start:
			if self.start_date < parse_date(start):
				return 0
		if end:
			if self.start_date > parse_date(end):
				return 0
		return self.quantity * self.fee

	def total_invoiced(self, start=None, end=None):
		if not self.invoice_sent_date:
			return 0
		if start:
			if self.invoice_sent_date < parse_date(start):
				return 0
		if end:
			if self.invoice_sent_date > parse_date(end):
				return 0
		return self.quantity * self.fee

class Payment(models.Model):

	class Meta:
		ordering = ('-date', 'amount')

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	date = models.DateField(default=timezone.now)
	amount = models.IntegerField()

	def __str__(self):
		return "{}: {}".format(self.invoice.payee.name, self.date)
