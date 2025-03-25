import random
import string
import accountManager
import postmanager

if __name__ != '__main__':
    print('this is not a module and should not be imported')
    exit(0)

accountManager.createAccount('user1', 'password1')
accountManager.createAccount('user2', 'password2')
accountManager.createAccount('user3', 'password3')
accountManager.createAccount('user4', 'password4')
accountManager.createAccount('user5', 'password5')
accountManager.createAccount('user6', 'password6')
accountManager.createAccount('user7', 'password7')
accountManager.createAccount('user8', 'password8')
accountManager.createAccount('user9', 'password9')
accountManager.createAccount('user10', 'password10')

POSTS = [
    {
        'user_id': i % 9+1,
        'content': ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(0, 100))),
        'likes': random.randint(0, 10000),
        'forwards': random.randint(0, 10000),
        'shares': random.randint(0, 10000)
    }

    for i in range(1, 1000)  # Generating 50 entries
]

for post in POSTS:
    postmanager.addPost(post)