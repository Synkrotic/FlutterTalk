from flask import render_template, request, Response
from sqlalchemy.orm import Session

from globals import *

import accountManager
import database
import secrets

from tables import User


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
    return getFullPage(
        render_template("viewAccount.html", displayName={accountManager.getOrDefaultUserName(accountManager.getUser(request))}, accountName=f'{accountName}', post=post))


@app.route('/users/addShare/<int:postID>')
def addShare(postID):
    post = getPost({accountManager.getOrDefaultUserName(accountManager.getUser(request))}, postID)
    if post is None:
        return "-1"

    post["sharedAmount"] += 1
    return str(post["sharedAmount"])


@app.route('/profile')
def viewProfile(new_token = None):
    response = Response()
    if new_token is not None:
        response.set_cookie('token', new_token, httponly=True)
        user: User = accountManager.getUser(new_token)
    else:
        user: User = accountManager.getUser(request)

    print ("user:", user)
    if user is None:
        response.set_data(getFullPage(render_template("viewProfile.html", action="login")))
        return response

    account = {
        "displayName": accountManager.getOrDefaultUserName(user),
        "accountName": accountManager.getOrDefaultUserName(user),
        "bio": user.bio,
        "location": user.location,
        "pfp": "https://i.pinimg.com/736x/c0/27/be/c027bec07c2dc08b9df60921dfd539bd.jpg",
    }
    response.set_data(getFullPage(render_template("viewProfile.html", user=account)))
    return response


@app.route('/login', methods=['POST'])
def login():
    token: str = accountManager.login(request.form['name'], request.form['password'])
    if token is not None:
        return viewProfile(token)
    else:
        return render_template("errorPage.html", error="Invalid login credentials")



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
    page = render_template("navbar.html", displayName={accountManager.getOrDefaultUserName(accountManager.getUser(request))},
                           accountName=f'{accountManager.getOrDefaultUserName(accountManager.getUser(request))}')
    page += renderedPage
    page += render_template("sidebar.html")
    return page


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=3000)