from handler import Handler
from utils.auth import *
from models.users import UserAccount
from models.blogpost import Purchase_Order
from google.appengine.ext import db


class purchase(Handler):
	def render_front(self, User = ""):
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
		self.render("purchase.html", User = User)
	
	@login_required
	def get(self):
		self.render_front()
	
	def post(self):
		User_id = self.request.cookies.get('user_id')
		Valid_User = check_secure_val(User_id)
		p  = UserAccount.get_by_id(int(Valid_User))
		User = p.User
		Address = self.request.get("Address")
		City = self.request.get("City")
		State = self.request.get("State")
		Country = self.request.get("Country")
		Quantity = self.request.get("Quantity")

		if User and Address and City and State and Country and Quantity:
			posts = Purchase_Order(User = User, Address = Address, City = City, State = State, Country=Country, Quantity=Quantity)
			posts.put()
			self.render("Thankyou.html", User = User)

		else:
			error = 'Please complete all the fields.'
			self.render("purchase.html", User=User, error = error)