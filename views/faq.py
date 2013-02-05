from handler import Handler
from utils.auth import *
from models.users import UserAccount
from google.appengine.ext import db


class faq(Handler):
	def render_front(self, User = "", error = ""):
		User_id = self.request.cookies.get('user_id')
		if User_id:
			Valid_User = check_secure_val(User_id)
			if Valid_User:
				p  = UserAccount.get_by_id(int(Valid_User))
				User = p.User
			else:
				User = ""
		else:
			User = ""
		self.render("faq.html", User = User, error = "")
	
	def get(self):
		self.render_front()
	