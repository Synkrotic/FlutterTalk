from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import Session, Query

import accountManager
import database
import postmanager
from globals import *
from tables import User, Authentication, Post, PostLike

@app.route('/')
def index():
    posts, cookies = postmanager.getPosts(10, request)
    response = Response(getFullPage(render_template("index.html", posts=posts)))
    return addCookiesToResponse(cookies, response)

@app.route('/users/@<string:accountName>/<int:postID>')
def viewPost(accountName, postId):
    post = postmanager.getPost(postId)
    
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
            post=post
        )
    )


@app.route('/users/@<string:accountName>')
def viewAccount(accountName):
    return accountName


@app.route('/users/addShare/<int:postID>')
def addShare(postID):
    session, postQuery = postmanager.getPostQuery(postID)
    
    if postQuery is None or postQuery.first() is None:
        return 400
    post: Post = postQuery.first()
    
    shares = post.shares
    postQuery.update({"shares": shares + 1})
    session.commit()
    return 200


@app.route('/users/like/<int:postID>', methods=['POST', 'DELETE', 'GET'])
def addLike(postID):
    session: Session
    postQuery: Query
    session, postQuery = postmanager.getPostQuery(postID)
    if postQuery is None or postQuery.first() is None:
        return 400
    match request.method:
        case 'DELETE':
            postLike = session.query(PostLike)\
                        .filter(PostLike.post_id == postID)\
                        .filter(PostLike.user_id == accountManager.getUser(request).id)\
                        .first()
            
            if postLike is None:
                return 400
            session.delete(postLike)
            session.commit()

        case 'POST':
            user = accountManager.getUser(request)
            if user is None:
                return 401
            if session.query(PostLike) \
                    .filter(PostLike.post_id == postID) \
                    .filter(PostLike.user_id == user.id) \
                    .first() is None:
                return 400
            
            postLike = PostLike(post_id=postID, user_id=user.id)
            session.add(postLike)
            session.commit()
    
    likes: int = session.query(PostLike).filter(PostLike.post_id == postID).count()
    postQuery.update({"likes": session.query(PostLike).filter(PostLike.post_id == postID).count()})
    session.commit()
    return str(likes)


@app.route('/profile')
def viewProfile():
    response = Response()
    user: User = accountManager.getUser(request)
    
    print("user:", user)
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
        response = app.redirect('/profile', code=302)
        response.set_cookie('token', token, httponly=True)
        return response
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


@app.route('/post', methods=['POST', 'GET'])
def createPost():
    if request.method == 'GET':
        return render_template("test.html")
    
    user = accountManager.getUser(request)
    if user is None:
        return redirect('/login')
    postmanager.addPost({
        "user_id": user.id,
        "content": request.form['content']
    }
    )
    
    return redirect('/')


@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/privacy")
def privacy():
    return redirect("https://bisquit.host/policy.pdf")

@app.route("/terms")
def tos():
    return redirect("https://bisquit.host/terms.pdf")

@app.route("/feedback")
def feedback():
    return redirect("mailto:topscrech@icloud.com")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errorPage.html", error="404 page not found!"), 404

def getFullPage(renderedPage):
    print(accountManager.getOrDefaultUserName(accountManager.getUser(request)))
    page = render_template("navbar.html",
                           displayName=accountManager.getOrDefaultUserName(accountManager.getUser(request)),
                           accountName=f'{accountManager.getOrDefaultUserName(accountManager.getUser(request))}'
                           )
    page += renderedPage
    page += render_template("sidebar.html")
    return page

if __name__ == '__main__':
    # database.create()
    app.run(debug=False, host='0.0.0.0', port=3000)