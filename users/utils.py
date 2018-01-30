def get_user_directory(self, filename):
	"""
	Directory of Avatar
	"""
	return 'profiles/{id}/{image}'.format(id=self.id, image=filename)

def get_company_directory(self, filename):
	"""
	Directory of Avatar
	"""
	return 'company/{id}/{image}'.format(id=self.id, image=filename)