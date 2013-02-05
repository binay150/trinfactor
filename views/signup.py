import re
from handler import Handler
from utils.auth import *
from google.appengine.ext import db
from models.users import UserAccount

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class SignUp(Handler):
	def render_front(self, username = "", password ="", verify = "", email = "", error_User="", error_Password = "", error_Verify= "", error_Email = "",User = "", error=""):
		self.render("signup.html", username = username, password = password, verify = verify, email = email, 
			error_User= error_User, error_Password = error_Password, error_Verify= error_Verify, error_Email = error_Email, User = "", error="")
	
	def get(self):
		self.render_front()
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')		
		
		if USER_RE.match(username):
			name_check = True
			error_User = ""
		else:
			name_check = False
			error_User = "That's not a valid username."
		
		if PASSWORD_RE.match(password):
			password_check = True
			error_Password = ""
			if password == verify:
				verify_check = True
				error_Verify = ""
			else:
				verify_check = False
				error_Verify = "Your passwords didn't match."
		else:
			password_check = False
			error_Password = "That wasn't a valid password."
			error_Verify = ""
			
		if email:
			if EMAIL_RE.match(email):
				email_check = True
				error_Email = ""
			else:
				email_check = False
				error_Email = "That's not a valid email."		
		else:
			email_check = True
			error_Email = ""	
			
		if email_check and password_check and verify_check and name_check:			
			Users = db.GqlQuery("SELECT * FROM UserAccount Where User = :1", username).get()
			if Users:
				error_User = "That user already exists."
				self.render_front(username, password, verify, email, error_User, error_Password, error_Verify, error_Email)	
			else:
				h = make_pw_hash(username, password)
				p = UserAccount(User = username, Password = h, Email = email)
				p.put()
				x = str(p.key().id())
				hashed_user = make_secure_val(x)
				self.response.headers.add_header('Set-Cookie', 'user_id=%s' %str(hashed_user))
				self.redirect("/welcome")
		else:
			self.render_front(username, password, verify, email, error_User, error_Password, error_Verify, error_Email, "","")
