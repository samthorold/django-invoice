from django.db import models


class Contact(models.Model):

	class Meta:
		ordering = ('name',)

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def total_payments(self, start=None, end=None):
		return sum(i.total_payment(start, end) for i in self.invoice_set.all())
