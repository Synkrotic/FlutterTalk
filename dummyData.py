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
    {'user_id': 1, 'content': 'Content of post 1', 'likes': 0, 'forwards': 0, 'shares': 0},
    {'user_id': 2, 'content': 'Content of post 2', 'likes': 999999, 'forwards': 21344, 'shares': 41},
    {'user_id': 3, 'content': 'Content of post 3', 'likes': 2, 'forwards': 4, 'shares': 0},
    {'user_id': 4, 'content': 'Content of post 4', 'likes': 3, 'forwards': 5, 'shares': 0},
    {'user_id': 5, 'content': 'Content of post 5', 'likes': 0, 'forwards': 12, 'shares': 0},
    {'user_id': 6, 'content': 'Content of post 6', 'likes': 0, 'forwards': 0, 'shares': 0},
    {'user_id': 7, 'content': 'Content of post 7', 'likes': 0, 'forwards': 0, 'shares': 0},
    {'user_id': 8, 'content': 'Content of post 8', 'likes': 0, 'forwards': 4, 'shares': 0},
    {'user_id': 9, 'content': 'Content of post 9', 'likes': 0, 'forwards': 0, 'shares': 0},
    {'user_id': 10, 'content': 'Content of post 10', 'likes': 0, 'forwards': 0, 'shares': 0},
]

for post in POSTS:
    postmanager.addPost(post)
