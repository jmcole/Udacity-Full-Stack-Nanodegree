from google.appengine.ext import db
from models.user import User
import utils


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    """Post database model"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    likes = db.IntegerProperty(default=0)
    liked_by = db.StringListProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    edited = db.BooleanProperty(default=False)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return utils.render_str("post.html", p=self)


class Comment(db.Model):
    """Comment Database Model"""
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    edited = db.BooleanProperty(default=False)
