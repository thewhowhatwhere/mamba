from app import application, db
from sqlalchemy import and_, desc
from app.auth.models import User
from app.site.models import PostComment

# Create the Models
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    text = db.Column(db.Text())
    published = db.Column(db.Boolean(), default=0)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    writen_by = db.Column(db.Integer(), db.ForeignKey('users.id'))
    comments = db.relationship('PostComment', backref='posts', lazy='joined')

    def get_blog(page):
        per_page = application.config["BLOG_PER_PAGE"]
        return Post.query.filter(Post.published==1).order_by(desc('posts_id')).paginate(page, per_page, error_out=False)

    def get_sortable_list(order, direction, page):
        per_page = application.config["ADMIN_PER_PAGE"]
        return Post.query.order_by(order+' ' +direction).paginate(page, per_page, error_out=False)

    def get_author(self):
        if self.writen_by:
            user = User.query.get(self.writen_by)
            if user:
                return user.get_display_name()
        return 'Unknown'

    def get_by_slug(slug):
        return Post.query.filter_by(slug=slug).first()

    def comment_count(self):
        return PostComment.query.filter(and_(PostComment.post==self.id, PostComment.published==1)).count()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    css = db.Column(db.Text())
    js = db.Column(db.Text())
    html = db.Column(db.Text())
    history = db.Column(db.Text())
    published = db.Column(db.Boolean(), default=0)

    def get_sortable_list(order, direction, page):
        per_page = application.config["ADMIN_PER_PAGE"]
        return Page.query.order_by(order+' ' +direction).paginate(page, per_page, error_out=False)

    def get_home_page():
        home_page = Page.query.filter(and_(Page.slug=='home', Page.published==1)).first()
        return home_page if home_page else None

    def get_page(slug):
        return Page.query.filter(Page.slug==slug).first()

    def get_pages():
        return Page.query.all()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()
