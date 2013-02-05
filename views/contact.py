from handler import Handler
from utils.auth import *
from models.users import UserAccount
from models.blogpost import Blogpost
from google.appengine.ext import db
from time import gmtime, strftime

class contact(Handler):
	def render_front(self, error = "", Blog_error=""):
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

		posts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		
		self.render("contact.html", User = User, error = "", 
			Blog_error = Blog_error, posts = posts )
	
	def get(self):		
		self.render_front()

	def post(self):
		User_id = self.request.cookies.get('user_id')
		Valid_User = check_secure_val(User_id)
		p  = UserAccount.get_by_id(int(Valid_User))
		User = p.User		
		newpost_bpost = self.request.get("content")
		posts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		if newpost_bpost:
			posts = Blogpost(bpost = newpost_bpost, user = User)
			posts.put()
			posts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
			self.render("contact.html", User = User, error="", posts = posts)

		else:
			error = "not a valid post"
			self.render("contact.html", User = User, error = "", posts = posts, Blog_error = "Please enter some text before submitting.")

	