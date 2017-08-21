from django.db import models
from django.utils import timezone


class WorkType(models.Model):

	class Meta:
		ordering = ('name',)

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def total_fees(self, start=None, end=None):
		fees = self.invoiceline_set
		if start:
			fees = fees.filter(date__gte=start)
		if end:
			fees = fees.filter(date__lte=end)
		return sum(il.total_fee(billable=False) for il in fees.all())

class Invoice(models.Model):

	payee = models.ForeignKey('contacts.Contact')
	notes = models.TextField(blank=True)

	def __str__(self):
		return self.payee.name

	def total_fee(self):
		return sum(il.total_fee() for il in self.invoiceline_set.all())

	def total_payment(self, start=None, end=None):
		payments = self.payment_set
		if start:
			payments = payments.filter(date__gte=start)
		if end:
			payments = payments.filter(date__lte=end)
		return sum(p.amount for p in payments.all())

	def fee_outstanding(self):
		return self.total_fee() - self.total_payment()

class InvoiceLine(models.Model):

	class Meta:
		ordering = ('-billable', 'work_type', '-date')

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	work_type = models.ForeignKey(WorkType)
	patient = models.ForeignKey('contacts.Contact')
	quantity = models.IntegerField()
	fee = models.IntegerField()
	date = models.DateField(default=timezone.now)
	billable = models.BooleanField()

	def __str__(self):
		return "{}: {}".format(self.work_type.name, self.patient.name)

	def total_fee(self, billable=True):
		if billable and not self.billable:
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
