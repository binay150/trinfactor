from handler import Handler

class Logout(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path = /')
		self.redirect("/")