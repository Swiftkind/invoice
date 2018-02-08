def get_client_company_logo_dir(self, filename):
    """ Directory of client company logo to be upload
    """
    return f"clients/company/{self.id}/{filename}"