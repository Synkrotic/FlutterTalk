from flask import Flask, render_template, make_response, request

import accountManager
import database, secrets
token_bytes: bytes = secrets.token_bytes()
token_hex: str = secrets.token_hex()
token_url: str = secrets.token_urlsafe()
print(token_bytes, token_hex, token_url)
app = Flask(__name__)

database.create()
@app.route('/')
def hello_world():  # put application's code here
    name = request.cookies.get('name')
    resp = make_response(render_template('test.html')) #name=name if name is not None else 'No name selected'))
    resp.set_cookie('name', 'U have a username now bitch')

    return resp


def valid_login(username, password):
    return username == 'admin' and password == 'secret'


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


if __name__ == '__main__':
    app.run()

@app.route('/post')
def post():
    print(request.form['name'])

