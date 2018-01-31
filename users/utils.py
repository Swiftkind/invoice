def get_user_directory(self, filename):
    """Directory of Avatar to be upload
    """
    return 'profiles/{id}/{image}'.format(id=self.id, image=filename)

def get_company_directory(self, filename):
    """Directory of Logo to be upload
    """
    return 'company/{id}/{image}'.format(id=self.id, image=filename)