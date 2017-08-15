from django.db import models


class WorkType(models.Model):

	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Invoice(models.Model):

	payee = models.ForeignKey('contacts.Contact')

	def __str__(self):
		return self.payee.name

class InvoiceLine(models.Model):

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	work_type = models.ForeignKey(WorkType)
	patient = models.ForeignKey('contacts.Contact')
	quantity = models.IntegerField()
	fee = models.IntegerField()
	billable = models.BooleanField()

	def __str__(self):
		return "{}: {}".format(self.work_type.name, self.patient.name)

class Payment(models.Model):

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	date = models.DateField()
	amount = models.IntegerField()

	def __str__(self):
		return "{}: {}".format(self.invoice.payee.name, self.date)
