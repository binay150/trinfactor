import webapp2
import cgi
import re
import os
import jinja2

import json
from time import gmtime, strftime
from models.users import UserAccount
from models.blogpost import Blogpost
from views import *

class PostHandler(Handler):
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
		self.render("notfound.html", User = User, error = "")
	
	def get(self, post_id):
		self.render_front("","")

class Post_JSON(Handler):
	def get(self, post_id):
		self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
		p = post_id
		posts  = Blogpost.get_by_id(int(p[:len(p)-5]))
		created = posts.created.strftime("%a %b %d %H:%M:%S %Y")
		json_output = {}
		json_output["content"] = posts.bpost
		json_output["subject"] = posts.title
		json_output["created"] = created
		self.response.out.write(json.dumps(json_output))

class Blog_JSON(Handler):
	def get(self):
		self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
		posts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		output = []
		for a in posts:
			created = a.created.strftime("%a %b %d %H:%M:%S %Y")
			json_output = {}
			json_output["content"] = a.bpost
			json_output["created"] = created
			json_output["subject"] = a.title
			output.append(json_output)
		self.response.out.write(json.dumps(output))

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/', MainPage),('/login', login),('/logout', Logout),
	('/signup', SignUp),('/welcome', Welcome),('/purchase', purchase),("/contact", contact), ('/firmware', firmware),('/hardware', hardware),('/([0-9]+.json)', Post_JSON),('/.json', Blog_JSON),('/faq', faq),
	(PAGE_RE, PostHandler),],debug=True)




 

