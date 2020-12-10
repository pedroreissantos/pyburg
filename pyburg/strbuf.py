class strbuf:
	def __init__(self):
		self.val=''
	def write(self,s):
		self.val+=s
	def __str__(self):
		return self.val
