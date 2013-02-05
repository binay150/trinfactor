
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
	created = db.DateProperty(auto_now_add = True)

class NewPost(Handler):
	def render_front(self, title = "", bpost ="", error="", blogpost = ""):
		self.render("NewPost.html", title = title, blogpost = blogpost, error = error)
	
	def get(self):
		self.render_front()
	
	def post(self):
		title = self.request.get("subject")
		bpost = self.request.get("content")
		
		if title and bpost:
			p = Blogpost(title = title, bpost = bpost)
			p.put()
			x = str(p.key().id())
			self.redirect("/%s"%x)
		else:
			error = "we need both a title and post!"
			self.render_front(title, bpost, error)
class MainPage(Handler):
	def render_front(self):
		posts = db.GqlQuery("SELECT * FROM Blogpost "
							"ORDER BY created DESC")
		self.render("list.html", posts = posts)
	def get(self):
		self.render_front()

class PostHandler(Handler):
	def get(self, post_id):
		p  = Blogpost.get_by_id(int(post_id))
		self.render("post.html", posts =  [p])

app = webapp2.WSGIApplication([('/', MainPage),('/newpost', NewPost),('/([0-9]+)', PostHandler)],debug=True)


 

