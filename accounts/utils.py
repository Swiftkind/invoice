def get_directory(self, filename):
	"""
	Directory of Avatar
	"""
	return 'profiles/{id}/{image}'.format(id=self.id, image=filename)