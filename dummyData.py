import random
import string
import accountManager
import postmanager

if __name__ != '__main__':
    print('this is not a module and should not be imported')
    exit(0)

users = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
passwords = ['password1', 'password2', 'password3', 'password4', 'password5', 'password6', 'password7', 'password8', 'password9', 'password10']

for i in range(len(users)):
    accountManager.createAccount(users[i], passwords[i])

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