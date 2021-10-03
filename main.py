import requests
from flask import Flask, render_template
app = Flask(__name__)

response = requests.get(url="https://api.npoint.io/88c2c1f644ef334058be").json()

@app.route("/")
def index():
    return render_template("index.html", blog_posts=response)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:num>")
def post_page(num):
    post_id = num - 1
    blog_page = response[post_id]
    return render_template("post.html", page=blog_page)

if __name__ == "__main__":
    app.run(debug=True)
