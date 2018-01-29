def get_invoice_directory(self, filename):
	return 'invoices/{id}/{pdf}'.format(id=self.id, pdf=filename)