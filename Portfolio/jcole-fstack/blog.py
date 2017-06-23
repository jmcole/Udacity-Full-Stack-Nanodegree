
import random
import time
import sys
import webapp2
import jinja2
import models.utils
from models.user import User as User
from models.blogdb import Post as Post
from models.blogdb import Comment as Comment
from google.appengine.ext import db


class BlogHandler(webapp2.RequestHandler):

    """Define login/logout cookie functions"""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return models.utils.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = models.utils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/'
                % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and models.utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie',
                'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class BlogFront(BlogHandler):

    """Render front.html"""

    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts=posts)


class PostPage(BlogHandler):

    """Creates individual blog post"""

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comment.all().order('-created')
        self.username = self.request.get('username')
        comments.filter('post_id =', post_id)
        if not post:
            self.error(404)
            return
        self.render('permalink.html', post=post, comments=comments)


class Signup(BlogHandler):

    """Handles user signup"""

    def get(self):
        self.render('signup-form.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username, email=self.email)

        if not models.utils.valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not models.utils.valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not models.utils.valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):

    """Registers new user"""

    def done(self):

        # make sure the user doesn't already exist

        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')


class Login(BlogHandler):

    """Handles user login"""

    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class Logout(BlogHandler):

    """Handles user logout"""

    def get(self):
        self.logout()
        self.redirect('/blog')


class NewPost(BlogHandler):

    """Creates new posts"""

    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect('/login')

    def post(self):
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(
                parent=blog_key(),
                subject=subject,
                author=self.user.name,
                content=content,
                edited=False,
                likes=0,
                )
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content, please!'
            self.render('newpost.html', subject=subject,
                        content=content, error=error)


class LikeHandler(BlogHandler):

    """Handles user likes"""

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            if post is None or post.liked_by.count(self.user) > 1:
                self.redirect('/blog')
                return
            else:
                if self.user.name not in post.liked_by \
                    and self.user.name != post.author:
                    post.likes += 1
                    post.liked_by.append(self.user.name)
                    post.put()
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                    self.redirect('/blog')
        else:
            self.redirect('/login')


class UnLikeHandler(BlogHandler):

    """Unlikes a liked post"""

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            if post is None:
                self.redirect('/blog')
                return
            else:
                if self.user.name in post.liked_by and self.user.name \
                    != post.author:
                    post.likes -= 1
                    post.liked_by.remove(self.user.name)
                    post.put()
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                    self.redirect('/blog')
        else:
            self.redirect('/login')


class DeletePost(BlogHandler):

    """Deletes Posts"""

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            if self.user.name == post.author and post is not None:
                post.delete()
                self.redirect('/blog')
            else:
                self.redirect('/login')
        else:
            self.redirect('/login')


class EditPost(BlogHandler):

    """Pulls posts and allows edits to be saved."""

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            if post is not None:
                self.render('editpost.html', subject=post.subject,
                            content=post.content)
            else:
                self.redirect('/blog')
        else:
            self.redirect('/login')

    def post(self, post_id):
        if self.user:
            subject = self.request.get('subject')
            content = self.request.get('content')
            if subject and content:
                key = db.Key.from_path('Post', int(post_id),
                        parent=blog_key())
                post = db.get(key)
                if self.user.name == post.author and post is not None:
                    post.subject = subject
                    post.content = content
                    post.edited = True
                    post.put()
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                    self.redirect('/blog')
        else:
            self.redirect('/login')


class NewComment(BlogHandler):

    """Creates a new Comment by associating a comment with post_id"""

    def get(self, post_id):
        if self.user and post_id is not None:
            self.render('newComment.html')
        else:
            self.redirect('/login')

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            content = self.request.get('content')
            if content and post is not None:
                comment = Comment(content=content,
                                  author=self.user.name,
                                  post_id=post_id)
                comment.put()
                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                error = 'Content, please!'
                self.render('newComment.html', content=content,
                            error=error)
        else:
            self.redirect('/login')


class DeleteComment(BlogHandler):

    """Deletes comment and redirects back to post page. Includes safechecks to
     ensure post can only be deleted by author."""

    def post(self, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id))
            comment = db.get(key)
            if self.user.name == comment.author and comment is not None:
                comment.delete()
                self.redirect('/blog/' + comment.post_id)
            else:
                self.redirect('/blog')
        else:
            self.redirect('/login')


class EditComment(BlogHandler):

    """Pulls comment and allows edits to be saved. Includes safechecks to ensure
    edits can only be made by author"""

    def get(self, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id))
            comment = db.get(key)
            self.render('editcomment.html', content=comment.content)
        else:
            self.redirect('/login')

    def post(self, comment_id):
        if self.user:
            content = self.request.get('content')
            if content:
                key = db.Key.from_path('Comment', int(comment_id))
                comment = db.get(key)
                if self.user.name == comment.author and comment \
                    is not None:
                    comment.content = content
                    comment.edited = True
                    comment.put()
                    self.redirect('/blog/' + comment.post_id)
                else:
                    self.redirect('/blog')
            else:
                error = 'Content, please!'
                self.render('newComment.html', content=content,
                            error=error)
        else:
            self.redirect('/login')


class MainPage(BlogHandler):

    """MainPage of portfolioi"""

    def get(self):
        self.render('index.html')


class AboutPage(BlogHandler):

    """Creates about page"""

    def get(self):
        self.render('about.html')


class TomatoePage(BlogHandler):

    """Creates tomatoe page"""

    def get(self):
        self.render('fresh_tomatoes.html')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/newpost', NewPost),
    ('/signup', Register),
    ('/login', Login),
    ('/logout', Logout),
    ('/about', AboutPage),
    ('/fresh_tomatoes', TomatoePage),
    ('/blog/likes/([0-9]+)', LikeHandler),
    ('/blog/unlikes/([0-9]+)', UnLikeHandler),
    ('/blog/deletePost/([0-9]+)', DeletePost),
    ('/blog/editpost/([0-9]+)', EditPost),
    ('/blog/NewComment/([0-9]+)', NewComment),
    ('/blog/DeleteComment/([0-9]+)', DeleteComment),
    ('/blog/EditComment/([0-9]+)', EditComment),
    ], debug = True)
