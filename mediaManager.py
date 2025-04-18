import os

from flask import Request
from werkzeug.utils import send_file

import database
import tables

ALLOWED_EXTENSIONS = {'MEDIA': ['jpg', 'jpeg', 'png', 'gif', 'webp']}

# Function to check allowed file extensions
def allowed_file(filename, fileType: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[fileType]

def getExtension(filename: str):
    return filename.rsplit('.', 1)[1].lower()

def postMedia(file, user: tables.User, fileType: str):
    if file is None:
        return None, 400
    
    if file.filename is None or file.filename == '':
        return None, 400
    
    if not allowed_file(file.filename, fileType):
        return None, 400

    with database.getSession() as session:
        media = tables.MediaEntry(user_id=user.id, media_type=getExtension(file.filename))
        session.add(media)
        session.commit()
        file.save(os.path.realpath(f"media/{media.id}.{getExtension(file.filename)}"))
        return media.id, 200
        

def getMediaURL(mediaId: int, fileType: str):
    if mediaId is None or fileType is None:
        return None
    with database.getSession() as session:
        media = session.query(tables.MediaEntry).filter(tables.MediaEntry.id == mediaId).first()
        if media is None:
            print("media not found", mediaId, fileType)
            return None
        if media.media_type not in ALLOWED_EXTENSIONS[fileType]:
            print("media type not allowed")
            return None
        return f"/media/{mediaId}.{media.media_type}"
    
    
def getMedia(url: str, fileType: str, request: Request):
    if not allowed_file(url, fileType):
        return None
    if os.path.exists(f"media/" +url):
        print(f"media/{url}")
        return send_file(f"media/" +url, environ=request.environ)
    print(os.path.exists(f"/media/" +url))
    
    return None