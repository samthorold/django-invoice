from django.db import models


class WorkType(models.Model):

	name = models.CharField(max_length=200)

class Invoice(models.Model):

	payee = models.ForeignKey('contacts.Contact')

class InvoiceLine(models.Model):

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	work_type = models.ForeignKey(WorkType)
	patient = models.ForeignKey('contacts.Contact')
	fee = models.IntegerField()
	billable = models.BooleanField()

class Payment(models.Model):

	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	date = models.DateField()
	amount = models.IntegerField()