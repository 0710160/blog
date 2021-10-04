import requests
import smtplib
from flask import Flask, render_template, request
app = Flask(__name__)

response = requests.get(url="https://api.npoint.io/88c2c1f644ef334058be").json()
MY_EMAIL = "xiiixxx@yahoo.com"
MY_PASSWORD = "wrxjixdcxhrthkjl"
connection = smtplib.SMTP("smtp.mail.yahoo.com", timeout=120)
connection.starttls()
connection.login(user=MY_EMAIL, password=MY_PASSWORD)

@app.route("/")
def index():
    return render_template("index.html", blog_posts=response)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def receive_data():
    if request.method == "GET":
        title_text = "Contact Me"
        return render_template("contact.html", title=title_text)
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="xlvi@mm.st",
            msg=f"Subject:New email from website\n\nMessage received from {name}:\n \
            {message}\nContact details: {email}  |  {phone}"
        )
        connection.close()
        title_text = "Your message has been sent."
        return render_template("contact.html", title=title_text)

@app.route("/post/<int:num>")
def post_page(num):
    post_id = num - 1
    blog_page = response[post_id]
    return render_template("post.html", page=blog_page)


if __name__ == "__main__":
    app.run()
