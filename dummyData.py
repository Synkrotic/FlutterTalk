import os
import pathlib
import random
import string

from sqlalchemy.orm import Session

import accountManager
import database
import globals
from posts import postmanager
import tables

def gen():
    print("Generating dummy data...")
    users = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
    passwords = ['password1', 'password2', 'password3', 'password4', 'password5', 'password6', 'password7', 'password8', 'password9', 'password10']
    
    session: Session = database.getSession()
    user = tables.User(**globals.ADMIN)
    session.add(user)
    session.commit()
    
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
        

def checkVersion():
    if not pathlib.Path('database/dbVersion.txt').is_file():
        with open('database/dbVersion.txt', 'w') as f_current:
            f_current.write('-1')
    
    if not pathlib.Path('data.sqlite').is_file():
        database.create()
        gen()
        with open('database/dbNewestVersion.txt', 'r') as f_newest:
            newest_version = f_newest.read().strip()
        with open('database/dbVersion.txt', 'w') as f_current:
            f_current.write(newest_version)
    else:
        with open('database/dbNewestVersion.txt', 'r') as f_newest:
            newest_version = f_newest.read().strip()
        
        with open('database/dbVersion.txt', 'r') as f_current:
            current_version = f_current.read().strip()
        
        if newest_version != current_version:
            print("Versions don't match! rebuilding database...")
            os.remove('data.sqlite')
            database.create()
            gen()
            with open('database/dbVersion.txt', 'w') as f_current:
                f_current.write(newest_version)