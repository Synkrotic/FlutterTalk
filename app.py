from flask import render_template, request, Response
from globals import *
from tables import User, Authentication

import accountManager
from globals import *
from tables import User, Authentication

accountManager.createAccount('syn', 'pwd')
print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab')


@app.route('/')
def index():
    return getFullPage(render_template("index.html", posts=Posts))

@app.route('/users/@<string:accountName>/<int:postID>')
def viewPost(accountName, postID):
    post = getPost(accountName, postID)

    if post is None:
        return render_template("errorPage.html", error="404 post not found!")

    return getFullPage(
        render_template(
            "viewAccount.html",
            displayName={
                accountManager.getOrDefaultUserName(
                    accountManager.getUser(request)
                )
            },
            accountName=f'{accountName}',
            post=post)
    )

@app.route('/users/@<string:accountName>')
def viewAccount(accountName):
    return accountName

@app.route('/users/addShare/<int:postID>')
def addShare(postID):
    post = getPost({accountManager.getOrDefaultUserName(accountManager.getUser(request))}, postID)

    if post is None:
        return "-1"

    post["sharedAmount"] += 1
    return str(post["sharedAmount"])

@app.route('/profile')
def viewProfile():
    response = Response()
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
        response = Response()
        response.set_cookie('token', token, httponly=True)
        redirect('/profile', 200, response)
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


@app.route('/logout', methods=['POST'])
def logout():
    if 'token' not in request.cookies:
        return 412

    token = request.cookies['token']

    with database.getSession() as session:
        session.query(Authentication).filter_by(token=token).delete()

    response = Response()
    response.delete_cookie('token', httponly=True)
    return response


@app.route("/test")
def test():
    return render_template("test.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errorPage.html", error="404 page not found!"), 404


def getFullPage(renderedPage):
    print(accountManager.getOrDefaultUserName(accountManager.getUser(request)))
    page = render_template("navbar.html", displayName=accountManager.getOrDefaultUserName(accountManager.getUser(request)),
                           accountName=f'{accountManager.getOrDefaultUserName(accountManager.getUser(request))}')
    page += renderedPage
    page += render_template("sidebar.html")
    return page

import os
import database

from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session

db_path = os.path.join(os.getcwd(), 'data.sqlite')
engine: Engine = create_engine(f'sqlite:///{db_path}', echo=True)

def getSession() -> Session:
    return Session(engine)

def getConnection() -> Connection:
    return engine.connect()

if __name__ == '__main__':
    # database.create()
    app.run(debug=False, host='0.0.0.0', port=3000)