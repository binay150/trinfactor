import hmac
import random
import string
import hashlib
import logging
from functools import wraps
from views import *
from views.handler import Handler
SECRET = "SeRiOuSlySecRet"
def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):        
        logging.warning(args[0].request.cookies.get('user_id'))
        return f(*args, **kwargs)
    return decorated_function
