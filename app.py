from flask import Flask, request, render_template
from flask_cors import CORS
import time
app = Flask(__name__)
CORS(app)

displayName = "Synkrotic"
accountName = "synkrotic"

def formatNumber(number):
  if number > 999999999:
    return f"{number/1000000000}b"
  elif number > 999999:
    return f"{number/1000000}m"
  elif number > 999:
    return f"{number/1000}k"
  return number

posts = [
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

def getPost(accountName, postID):
  post = next((post for post in posts if post["postID"] == postID and post["accountName"] == accountName), None)
  return post

def getFullPage(renderedPage):
  page = render_template("navbar.html", displayName=displayName, accountName=f'@{accountName}')
  page += renderedPage
  page += render_template("sidebar.html")
  return page



@app.route('/')
def index():
  return getFullPage(render_template("index.html", posts=posts))


@app.route('/search')
def viewSearchPage():
  return getFullPage("")
  

@app.route('/notifications')
def viewNotificationsPage():
  return getFullPage("")
  

@app.route('/messages')
def viewMessagesPage():
  return getFullPage("")
  

@app.route('/feeds')
def viewFeedsPage():
  return getFullPage("")
  

@app.route('/lists')
def viewListsPage():
  return getFullPage("")
  

@app.route('/profile')
def viewProfilePage():
  return getFullPage("")
  

@app.route('/settings')
def viewSettingsPage():
  return getFullPage("")
  

@app.route('/createPost')
def viewCreatePostPage():
  return getFullPage("")
  

@app.route('/feedback')
def viewFeedbackPage():
  return getFullPage("")
  

@app.route('/privacy')
def viewPrivacyPage():
  return getFullPage("")
  

@app.route('/terms')
def viewTermsPage():
  return getFullPage("")
  

@app.route('/help')
def viewHelpPage():
  return getFullPage("")
  





@app.route('/users/@<string:accountName>/<int:postID>')
def viewPost(accountName, postID):
  post = getPost(accountName, postID)
  if not post:
    return render_template("errorPage.html", error="404 post not found!")
  return getFullPage(render_template("viewAccount.html", displayName=displayName, accountName=f'@{accountName}', post=post))





@app.route('/users/@<string:accountName>/<int:postID>/addShare')
def addShare(accountName, postID):
  post = getPost(accountName, postID)
  if not post:
    return False
  
  post["sharedAmount"] += 1
  return str(post["sharedAmount"])


@app.errorhandler(404)
def page_not_found(e):
  return render_template("errorPage.html", error="404 page not found!"), 404




if __name__ == '__main__':
  app.run(debug=True, port=5500)