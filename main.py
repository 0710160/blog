from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import bleach


def bleach_html(content):
    '''
    Strips html of any script injections
    '''
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']

    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }

    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)
    return cleaned


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b1'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    return render_template("post.html", post=requested_post)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    if request.method == "GET":
        edit_or_new = "Edit"
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        return render_template("make-post.html", post_id=post_id, form=edit_form, edit_or_new=edit_or_new)
    if request.method == "POST":
        ckeditor_output = request.form.get('body')
        post = BlogPost(
            id=post.id,
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            date=post.date,
            author=request.form['author'],
            img_url=request.form['img_url'],
            body=bleach_html(ckeditor_output)
        )
        db.session.commit()
        return render_template("post.html", post=post)


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        form = CreatePostForm()
        edit_or_new = "New"
        return render_template("make-post.html", form=form, edit_or_new=edit_or_new)
    if request.method == "POST":
        ckeditor_output = request.form.get('body')
        new_blog_post = BlogPost(
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            date=datetime.today().strftime('%m %d, %Y'),
            author=request.form['author'],
            img_url=request.form['img_url'],
            body=bleach_html(ckeditor_output)
        )
        db.session.add(new_blog_post)
        db.session.commit()
        posts = BlogPost.query.all()
        return render_template("index.html", all_posts=posts)


@app.route("/delete/<post_id>")
def delete(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    #app.run(host='10.0.1.26', port=5000)
    app.run(debug=True)
