import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	


class Blogpost(db.Model):
	title = db.StringProperty(required = True)
	bpost = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def render_front(self, title = "", bpost ="", error=""):
		arts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		self.render("front.html", title = title, blogpost=blogpost, error = error, arts = arts)
	
	def get(self):
		self.render_front()
	
	def post(self):
		title = self.request.get("title")
		bpost = self.request.get("boost")
		
		if title and art:
			p = Blogpost(title = title, bpost = bpost)
			p.put()
			x = str(p.key().id())
			self.redirect("/%s"%x)
		else:
			error = "we need both a title and some artwork!"
			self.render_front(title, bpost, error)
	



app = webapp2.WSGIApplication([('/blog', MainPage),('([0-9]+)', PostHandler)],debug=True)

Class PostHandler(Handler):
	def get(self, post_id):
		p  = Blogpost.get_by_id(post_id)
		if p:
			render_front()
	
	def render_front(self, title = "", bpost ="", error=""):
		arts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		self.render("front.html", title = title, blogpost=blogpost, error = error, arts = arts)

	p = Post(t,c)
	p.put()
	x = str(p.key().id())
	self.redirect('/blog/%s' %x)

 
