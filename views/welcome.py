
from handler import Handler
from utils.auth import *
from models.users import UserAccount
class Welcome(Handler):
	def get(self):
		User_id = self.request.cookies.get('user_id')
		Valid_User = check_secure_val(User_id)
		if Valid_User:
			p  = UserAccount.get_by_id(int(Valid_User))
			self.render("welcome.html", User =  p.User)
		else:
			self.redirect("/signup")