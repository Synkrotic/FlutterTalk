from enum import Enum

from sqlalchemy import and_, union, or_

import database
from tables import Post, User



def search(searchTerm: str, session):
    split = searchTerm.split(" ")
    if split == []:
        return None
    all_posts = []
    for term in split:
        if term.startswith('@'):
            term = term[1:]
            all_posts.append( session.query(Post).join(Post.user).where( User.account_name.contains(term)) )
        else:
            all_posts.append( session.query(Post).where( Post.content.contains(term)) )
    
    if len(all_posts) == 0:
        return None
    if len(all_posts) == 1:
        return all_posts[0]
    all_posts = all_posts[0].union(*all_posts[1:])
    return all_posts
    
       