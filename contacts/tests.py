from django.test import TestCase

from .models import Contact


class ContactModelTests(TestCase):

	def test_name(self):
		contact = Contact(name='Brian Dawes')
		self.assertIs(contact.name, 'Brian Dawes')
