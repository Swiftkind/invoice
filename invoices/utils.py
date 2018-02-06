def get_invoice_directory(self, filename):
    """ Directory upload pdf
    """
    return f'invoices/{self.id}/{filename}'