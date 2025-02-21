from flask import Flask, render_template
from flask_cors import CORS
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

@app.route('/')
def index():
  page = render_template("navbar.html", displayName=displayName, accountName=f'@{accountName}')
  page += render_template("index.html", posts=posts)
  page += render_template("sidebar.html")
  return page

@app.route('/users/@<string:accountName>/<int:postID>')
def viewPost(accountName, postID):
  post = next((post for post in posts if post["postID"] == postID and post["accountName"] == accountName), None)
  if not post:
    return render_template("errorPage.html", error="404 post not found!")
  return render_template("viewAccount.html", displayName=displayName, accountName=f'@{accountName}', post=post)

@app.route('/users/@<string:accountName>/<int:postID>/addShare')
def addShare(accountName, postID):
  post = next((post for post in posts if post["postID"] == postID and post["accountName"] == accountName), None)
  if not post:
    return False
  
  post["sharedAmount"] += 1
  return str(post["sharedAmount"])

if __name__ == '__main__':
  app.run(debug=True, port=5500)