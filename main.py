# Lession 4.7: Introducing Templates

# We introduce templates to build complicated strings using the Jinja2 library.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4186408748/m-686598825

import os

import jinja2
import webapp2

from google.appengine.ext import ndb

# Set up jinja environment
template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# Create global variables for database and current user
comments_database = 'comments'
current_user = "Anonymous"

def valid_user_name(user_name):
    """ Validate user name. username with digits and alphabets allowed """
    for ch in user_name:
        if not (ch.isdigit() or ch.isalpha()):
            print "Return False"
            return False
    return True

def comments_key(database=comments_database):
    """Constructs a Datastore key for a comments entity.
    """
    return ndb.Key('Comments', database)

class Comment(ndb.Model):
    """A main model for representing an individual comment entry."""
    user = ndb.StringProperty(indexed = False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    """ Main Handler class to render all the HTML pages """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    """ Handler class for "/*" documents """
    def get(self):
        comments_query = Comment.query(
            ancestor=comments_key(comments_database)).order(-Comment.date)
        number_of_comments = 10
        comments_list = comments_query.fetch(number_of_comments)
        global current_user
        if current_user == "Anonymous":
            user_status = "Login"
        else:
            user_status = "Logout"

        self.render("my_first.html", user_status = user_status, user_name = current_user, comments_list = comments_list)

class LoginPageLoader(Handler):
    """ Class for /login """
    def get(self):
        self.render("login.html", text = "")

    def post(self):
        user_name = self.request.get("user_name")
        if not user_name:
            self.render("login.html", text = "Please enter a name in the text box")
        elif valid_user_name(user_name):
            global current_user
            current_user = user_name
            self.redirect("/")
        else:
            self.render("login.html", text = "Please enter a valid name in the text box. A valid name is a combination of digits and alphabets")


class PostPageLoader(Handler):
    """ Class for /post """
    def post(self):
        comments_data = Comment(parent=comments_key(comments_database))
        comments_data.user = current_user
        comments_data.content = self.request.get("content")
        if comments_data.content:
            comments_data.put()
        self.redirect("/#comments")

class LogOutPageLoader(Handler):
    """ Class for /logout """
    def post(self):
        global current_user
        current_user = "Anonymous"
        self.redirect("/")

app = webapp2.WSGIApplication([("/", MainPage), ("/login", LoginPageLoader), ("/post", PostPageLoader), ("/logout", LogOutPageLoader)])
