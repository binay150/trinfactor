from handler import Handler
from utils.auth import *
from google.appengine.ext import db
from models.users import UserAccount
import logging
class login(Handler):
	def render_front(self, User = "", username = "", password ="", error = ""):
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
		self.render("login.html", User = "", username = username, password = password, error = error)
		
	@login_required
	def get(self):
		self.render_front()
	
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		if username:
			if password:
				Users = db.GqlQuery("SELECT * FROM UserAccount Where User = :1", username).get()
				if Users:
					password_recorded = Users.Password
					if valid_pw(username, password, password_recorded):
						x = str(Users.key().id())
						hashed_user = make_secure_val(x)
						self.response.headers.add_header('Set-Cookie', 'user_id=%s' %str(hashed_user))	
						self.redirect("/welcome")

					else:
						error = 'Invalid Username and / or Password'
						self.render_front("",username, password, error) 
				else:
					error = 'Invalid Username and / or Password'
					self.render_front("",username, password, error)
			else:
				error = 'Please Enter your Password.'
				self.render_front("",username, password, error)
		else:
			error = 'Please Enter your Username.'
			self.render_front("",username, password, error)