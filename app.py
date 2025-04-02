import random
from flask import render_template, request, redirect # type: ignore
import dummyData

import accountManager
import database
from globals import *
from posts import postmanager, postData
from posts.postData import getLike
from search import search
from tables import User, Authentication

errors = [] #* [id, {"type": "", "text": ""}]


@app.route('/getHTMLFile/<string:filename>', methods=['POST'])
def getHTMLFile(filename: str):
    with open(f"templates/{filename}", 'r', encoding="utf-8") as file:
        return file.read(), 200


@app.route('/')
def index():
    posts, _ = postmanager.getPosts(10, request)
    response = Response(getFullPage(render_template("index.html", posts=posts)))

    response.set_cookie("current_post", '0')
    return response



@app.route('/getPosts/<int:amount>')
def getPosts(amount: int):
    if request.args.get('query') is not None:
        posts, cookies = postmanager.getPosts(amount, request, search(request.args.get('query')))
    else:
        posts, cookies = postmanager.getPosts(amount, request)
    response = Response(json.dumps(posts))

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
    
    return getFullPage(
        render_template(
            "viewPost.html",
            post=post
        )
    )


@app.route('/users/@<string:accountName>')
def viewAccount(accountName):
    if not accountManager._checkExists(accountName):
        return render_template("errorPage.html", error="404 user not found!")
    
    user: User = accountManager.getUserByName(accountName)

    if user is None:
        return render_template("errorPage.html", error="404 user not found!")
    
    posts, _ = postmanager.getPostsOfUserByID(user.id, 10, request)
    response = Response(getFullPage(render_template("index.html", posts=posts)))
    
    response.set_cookie("current_post", '0')
    return response


@app.route('/posts/addShare/<int:postId>')
def addShare(postId):
    return postData.addShare(postId, accountManager.getUser(request))


@app.route('/users/like/<int:postID>', methods=['POST', 'DELETE', 'GET'])
def likePost(postID):
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


@app.route('/profile')
@app.route('/profile/<string:action>')
def viewProfile(action="login"):
    response = Response()
    user: User = accountManager.getUser(request)

    if user is None:
        response.set_data(getFullPage(render_template("viewProfile.html", action=action)))
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


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/settings")
def settings():
    return getFullPage(render_template("settings.html"))


@app.route("/closePopup/<int:errorID>", methods=['POST'])
def closePopup(errorID):
    try:
        for error in errors:
            if error[0] == errorID:
                errors.remove(error)
                break

    except IndexError:
        return "Error: No popup with this ID found!", 404

    return "Successfully closed the popup!", 200

CurrentErrorId = 0
@app.route("/addPopup/<string:errorType>/<string:error>", methods=['POST'])
def addPopup(errorType, error):
    global CurrentErrorId
    CurrentErrorId += 1
    errors.append([CurrentErrorId, {"type": errorType, "text": error}])
    return render_template('popup.html', popupType=errorType, errorID=str(CurrentErrorId), errorText=error), 200


@app.route("/postMedia")
def postMedia():
    postMedia(request)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errorPage.html", error="404 page not found!"), 404


def getFullPage(renderedPage):
    print(accountManager.getOrDefaultUserName(accountManager.getUser(request)))
    
    page = render_template("siteInitialization.html", errors=errors)
    page += render_template(
        "navbar.html",
        displayName=accountManager.getOrDefaultUserName(accountManager.getUser(request)),
        accountName=f'{accountManager.getOrDefaultUserName(accountManager.getUser(request))}'
    )
    
    page += renderedPage
    page += render_template("sidebar.html")
    return page

if __name__ == '__main__':
    dummyData.checkVersion()

    app.run(debug=True, host='0.0.0.0', port=3000)