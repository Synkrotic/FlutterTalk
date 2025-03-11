from globals import *

@app.route('/getPost/<str:authToken>', methods=['GET'])
def feed(authToken: str) -> str:
    return getFullPage(render_template("index.html", posts=Posts))