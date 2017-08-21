from django.db import models
from invoice.models import Payment

class Contact(models.Model):

	class Meta:
		ordering = ('name',)

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	@property
	def payments(self):
		return Payment.objects.filter(invoice__payee=self)

	def total_payments(self, start=None, end=None):
		return sum(i.total_payment(start, end) for i in self.invoice_set.all())
