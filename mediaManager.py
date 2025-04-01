from flask import Request, session

import accountManager
import database
import tables



def postMedia(request: Request):
    file = request.files.get('file')
    entry = tables.MediaEntry(user=accountManager.getUser(request), file=file.read())
    with database.getSession() as session:
        session.add(tables.MediaEntry(file=file.read(),
                                 user=accountManager.getUser(request),)
        session.commit()