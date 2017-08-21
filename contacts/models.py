from django.db import models


class Contact(models.Model):

	class Meta:
		ordering = ('name',)

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def total_payments(self, start=None, end=None):
		return sum(i.total_payment(start, end) for i in self.invoice_set.all())

	def total_fees(self, start=None, end=None):
		return sum(i.total_fee(start, end) for i in self.invoice_set.all())

	def total_invoiced(self, start=None, end=None):
		return sum(i.total_invoiced(start, end) for i in self.invoice_set.all())
