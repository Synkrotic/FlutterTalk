import random

from flask import render_template, request, redirect, flash  # type: ignore

import accountManager
import database
import dummyData
import mediaManager
import userData
from forms import UpdateProfileForm
from globals import *
from posts import postmanager, postData
from posts.postData import getLike
from tables import User, Authentication



@app.route('/getHTMLFile/<string:filename>', methods=['GET'])
def getHTMLFile(filename: str):
    with open(f"templates/{filename}", 'r', encoding="utf-8") as file:
        return file.read(), 200


@app.route('/')
def index():
    posts, _ = postmanager.getPosts(10, request)
    response = Response(getFullPage(render_template("index.html", posts=posts), 0))
    response.set_cookie("current_post", '10')
    response.cache_control.no_store = True

    return response


@app.route('/getPosts/<int:amount>')
def getPosts(amount: int):
    posts, cookies = postmanager.getPosts(amount, request)
    response = Response(json.dumps(posts))
    response.cache_control.no_store = True
    return addCookiesToResponse(cookies, response)


@app.route('/users/isLoggedIn', methods=['GET'])
def isLoggedIn():
    user = accountManager.getUser(request)
    if user is None:
        return json.dumps({'logged_in':False, 'username': None}), 200
    return json.dumps({'logged_in':True, 'username': accountManager.getOrDefaultUserName(user)}), 200


@app.route('/posts/view/<int:postId>')
def viewPost(postId):
    post = postmanager.getPostDict(postId, request)    
    if post is None:
        return render_template("errorPage.html", error="404 post not found!")

    user: User = accountManager.getUserByName(post.get('accountName'))
    if user is None:
        return render_template("errorPage.html", error="404 post not found!")

    account = userData.getUserDict(user)

    return getFullPage(
        render_template(
            "viewPost.html",
            account=account,
            post=post
        )
    )


@app.route('/users/@<string:accountName>')
def viewAccount(accountName):
    if not accountManager.checkExists(accountName):
        return render_template("errorPage.html", error="404 user not found!")
    
    user: User = accountManager.getUserByName(accountName)

    if user is None:
        return render_template("errorPage.html", error="404 user not found!")
    
    account = userData.getUserDict(user)

    posts, _ = postmanager.getPostsOfUserByID(user.id, 10, request)
    response = Response(getFullPage(render_template("viewAccount.html", account=account, posts=posts)))
    
    response.set_cookie("current_post", '0')
    return response


@app.route('/posts/addShare/<int:postId>')
def addShare(postId):
    return postData.addShare(postId, accountManager.getUser(request))


@app.route('/users/follow/<string:accountName>', methods=['POST', 'DELETE', 'GET'])
def follow(accountName):
    user: User = accountManager.getUser(request)
    if user is None:
        return render_template("errorPage.html", error="You need to be logged in!"), 404
    userToFollow = accountManager.getUserByName(accountName)
    if userToFollow is None:
        return render_template("errorPage.html", error="Tried to follow a non existing user!"), 401
    if user.id == userToFollow.id:
        return render_template("errorPage.html", error="You cannot follow yourself!"), 403

    match request.method:
        case 'DELETE':
            return json.dumps(userData.removeFollowing(user, userToFollow))
        case 'POST':
            return json.dumps(userData.addFollowing(user, userToFollow))
        case 'GET':
            return json.dumps(userData.getFollowing(user, userToFollow))
        case _:
            return render_template("errorPage.html", error="Invalid method used")


@app.route('/users/like/<int:postID>', methods=['POST', 'DELETE', 'GET'])
def like(postID):
    user: User = accountManager.getUser(request)
    match request.method:
        case 'DELETE':
            return postData.deleteLike(postID, user)
        case 'POST':
            return postData.addLike(postID, user)
        case 'GET':
            return getLike(postID, user)
        case _:
            return render_template("errorPage.html", error="Invalid method used")


@app.route('/search')
def searchPosts():
    return getFullPage(render_template("search.html"), 1)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<string:action>', methods=['GET', 'POST'])
def viewProfile(action="login"):
    response = Response()
    user: User = accountManager.getUser(request)

    if user is None:
        response.set_data(getFullPage(render_template("viewProfile.html", action=action), 6))
        return response
    
    account = userData.getUserDict(user)
    if request.method == 'POST':
        status, result = accountManager.updateProfile(request)
        if status == 'name_exists':
            addPopup('error', 'Name already exists!', response)
        elif status == 'success':
            account = result
            addPopup('success', 'Profile updated! changes take affect after a while.', response)
        elif status == 'error':
            addPopup('error', 'Error updating profile!', response)
        
        
    form = UpdateProfileForm()
    response.set_data(getFullPage(render_template("viewProfile.html", user=account, form=form), 6))
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


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if accountManager.createAccount(request.form['name'], request.form['password']):
            addPopup('success', 'Account created!')
            token: str = accountManager.login(request.form['name'], request.form['password'])

            response: Response = redirect('profile')
            return response
        else:
            addPopup('error', 'Account already exists.')
            return redirect('profile/register')


@app.route('/logout', methods=['POST'])
def logout():
    if 'token' not in request.cookies:
        return json.dumps({"errorText": "User not logged in!"}), 412, {'ContentType': 'application/json'}
    
    token = request.cookies['token']
    
    with database.getSession() as session:
        session.query(Authentication).filter_by(token=token).delete()
    
    response = Response()
    response.delete_cookie('token', httponly=True)
    return response


@app.route('/post', methods=['POST'])
@app.route('/post/<int:parentId>', methods=['POST'])
def createPost(parentId=None):
    user = accountManager.getUser(request)
    if user is None:
        return json.dumps({"statusText": "User is not logged in!"}), 401, { "ContentType": 'application/json' }
    
    content = list(request.get_json().values())[0]

    postId = postmanager.addPost({
        "has_parent": parentId is not None,
        "user_id": user.id,
        "content": content
    })
    
    if parentId is not None:
        postData.linkComment(parentId, postId)

    return redirect('/'), 200 # TODO miss redirecten naar de post zelf (/users/@<accountName>/<postID>)




@app.route("/media", methods=['POST'])
def postMedia():
    response = mediaManager.postMedia(request.files.get('file'), accountManager.getUser(request), 'MEDIA')
    if response[1] == 200:
        return json.dumps({'id':response[0], 'success':True}), 200
    return json.dumps({'id':response[0], 'success':False}), 400


@app.route("/media/<string:url>", methods=['GET'])
def getMedia(url):
    response = mediaManager.getMedia(url, 'MEDIA', request)
    return (response, 200) if response is not None else (json.dumps({'success':False}), 400)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errorPage.html", error="404 page not found!"), 404


def addPopup(errorType, error, response=None):
    if not response:
        response = Response()

    errorID = random.randint(0, 1_000_000_000)
    popupInfo = {
        "type": errorType,
        "text": error
    }
    response.set_cookie(f"POPUP-{errorID}", str(popupInfo))
    return response


def getFullPage(renderedPage, activePageID=-1):
    page = render_template("siteInitialization.html")
    user = accountManager.getUser(request)
    pfp = mediaManager.getMediaURL(user.profile_pic if user is not None else None, "MEDIA") if user is not None else DEFAULT_PFP
    page += render_template(
        "navbar.html",
        displayName=accountManager.getOrDefaultDisplayName(accountManager.getUser(request)),
        pfp=pfp if pfp is not None else DEFAULT_PFP,
        accountName=f'{accountManager.getOrDefaultUserName(accountManager.getUser(request))}',
        activeID=activePageID
    )
    
    page += renderedPage
    # page += render_template("sidebar.html")
    return page


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


@app.route("/settings")
def settings():
    return getFullPage(render_template("settings.html"), 7)


if __name__ == '__main__':
    dummyData.checkVersion()
    app.config['SECRET_KEY'] = 'FLUTTERTALK_ADMIN_KEY'
    app.config['SQLALCHEMY_POOL_SIZE'] = 300
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 500
    app.run(debug=True, host='0.0.0.0', port=3000)
