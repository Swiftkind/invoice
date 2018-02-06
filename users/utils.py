def get_user_directory(self, filename):
    """Directory of Avatar to be upload
    """
    return "profiles/{self.id}/{filename}"

def get_company_directory(self, filename):
    """Directory of Logo to be upload
    """
    return f"company/{self.id}/{filename}"