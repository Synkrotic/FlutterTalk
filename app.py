from flask import render_template, request
from globals import *

import accountManager
import database
import secrets

DisplayName = "Synkrotic"
AccountName = "synkrotic"
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

#database.create()
accountManager.createAccount('syn', 'pwd')
def getFullPage(renderedPage):
    print(request.cookies.get('token'))
    page = render_template("navbar.html",
                           displayName=DisplayName,
                           accountName=accountManager.getOrDefaultUserName(accountManager.getUser(request))
    )
    page += renderedPage
    page += render_template("sidebar.html")
    return page

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
  return getFullPage(render_template("viewAccount.html", displayName=displayName, accountName=f'{accountName}', post=post))
    post = getPost(accountName, postID)
    if post is None:
        return render_template("errorPage.html", error="404 post not found!")
    return getFullPage(render_template("viewAccount.html", displayName=DisplayName, accountName=f'@{accountName}', post=post))


@app.route('/users/addShare/<int:postID>')
def addShare(postID):
    post = getPost(AccountName, postID)
    if post is None:
        return "-1"

    post["sharedAmount"] += 1
    return str(post["sharedAmount"])


@app.route('/profile')
def viewProfile():
    if AccountName is not None:
        return getFullPage(render_template("viewProfile.html", displayName=DisplayName, accountName=f'@{AccountName}'))

    return getFullPage(render_template("errorPage.html", error="401 unauthorized"))
  # TODO Get accountdetails from database
  account = {
    "displayName": "Synkrotic",
    "accountName": "synkrotic",
    "password": "password",
    "bio": "Cheesecake",
    "location": "The Netherlands",
    "pfp": "https://i.pinimg.com/736x/c0/27/be/c027bec07c2dc08b9df60921dfd539bd.jpg",
  }
  if account is None:
    return getFullPage(render_template("viewProfile.html", action="login")) # either login or register (NOT CAPITALIZED!!!)
  return getFullPage(render_template("viewProfile.html", user=account))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return accountManager.login(request.form['name'], request.form['password'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if accountManager.createAccount(request.form['name'], request.form['password']):
            return 'account created'
        else:
            return 'account already exists'
    else:
        return render_template('register.html')

@app.route("/test")
def test():
    return render_template("test.html")


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
