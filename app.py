from flask import render_template, request
from globals import *

import accountManager
import database
import secrets

token_bytes: bytes = secrets.token_bytes()
token_hex: str = secrets.token_hex()
token_url: str = secrets.token_urlsafe()
print(token_bytes, token_hex, token_url)
displayName = "Synkrotic"
accountName = "synkrotic"
Posts = [
  {
    "postID": 1,
    "displayName": "Pufferenco",
    "accountName": "pufferenco",
    "content": "Hello, World!",
    "age": "3h",
    "commentAmount": 2,
    "sharedAmount": 3,
    "likeAmount": 10,
    "liked": True
  },
  {
    "postID": 1,
    "displayName": "JaneDoe",
    "accountName": "janedoe",
    "content": "Just finished my project! I'm really excited about the progress I've made and looking forward to what comes next.",
    "age": "1h",
    "commentAmount": 4,
    "sharedAmount": 1,
    "likeAmount": 20,
    "liked": False
  },
  {
    "postID": 1,
    "displayName": "TechGuru",
    "accountName": "techguru",
    "content": "Exploring new technologies and frameworks is my passion. From Python to web development, I love diving deep into code and sharing insights with the community!",
    "age": "30m",
    "commentAmount": 1,
    "sharedAmount": 0,
    "likeAmount": 30,
    "liked": True
  }
]

database.create()

def getPost(accountName, postID):
  post = next((post for post in Posts if post["postID"] == postID and post["accountName"] == accountName), None)
  return post


@app.route('/')
def index():
  return getFullPage(render_template("index.html", posts=Posts))


@app.route('/users/@<string:accountName>/<int:postID>')
def viewPost(accountName, postID):
  post = getPost(accountName, postID)
  if post is None:
    return render_template("errorPage.html", error="404 post not found!")
  return getFullPage(render_template("viewAccount.html", displayName=displayName, accountName=f'@{accountName}', post=post))


@app.route('/users/addShare/<int:postID>')
def addShare(postID):
    post = getPost(accountName, postID)
    if post is None:
        return "-1"

    post["sharedAmount"] += 1
    return str(post["sharedAmount"])


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if accountManager.login(request.form['name'], request.form['password']):
            return 'logged in'
        else:
            return 'username or password incorrect'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if accountManager.createAccount(request.form['name'], request.form['password']):
            return 'account created'
        else:
            return 'account already exists'
    else:
        return render_template('register.html')


@app.errorhandler(404)
def page_not_found(e):
  return render_template("errorPage.html", error="404 page not found!"), 404


def getFullPage(renderedPage):
  page = render_template("navbar.html", displayName=displayName, accountName=f'@{accountName}')
  page += renderedPage
  page += render_template("sidebar.html")
  return page

if __name__ == '__main__':
    app.run(debug=True)
