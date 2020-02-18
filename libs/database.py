import psycopg2

from automommy import secrets

"""
Interact with the database to find what shows are available.
"""

class DatabaseController():
    
    connection = None
    
    def __init__(self):

        self.connection = psycopg2.connect(user = secrets.username,
                                           password = secrets.password,
                                           host = secrets.host,
                                           port = secrets.port,
                                           database = secrets.database)

    """
    Fetch an instance of a show from the database
    """
    def fetchShow(self, showName):
        cursor = self.connection.cursor()
        show_sql = "SELECT * FROM shows WHERE name = %s"
        links_sql = "SELECT * FROM links WHERE show = %s"
        lastshown_sql = "SELECT * FROM lastshown WHERE show = %s"
        cursor.execute(show_sql, (showName,))
        show = cursor.fetchone()

        if not show:
            return None
        
        cursor.execute(links_sql, (show[0],))
        link = cursor.fetchone()

        cursor.execute(lastshown_sql, (show[0],))
        lastshown = cursor.fetchone()

        hasExternal = True if link else False

        return ShowEntity(show[0], show[3], show[2], show[4], hasExternal, self.lastWatched(show[0]))

    """
    Find the id of the last shown episode of a show
    """
    def lastWatched(self, showid):
        cursor = self.connection.cursor()
        lastshown_sql = "SELECT lastid FROM lastshown WHERE show = %s"
        cursor.execute(lastshown_sql, (showid,))
        lastshown = cursor.fetchone()

        return lastshown[0]

    """
    Find the first episode of a show, we're assuming the database is ordered
    """
    def firstEpisode(self, showid):
        cursor = self.connection.cursor()
        firstshown_sql = "SELECT linkid FROM links WHERE show = %s"
        cursor.execute(firstshown_sql, (showid,))

        firstshown = cursor.fetchone()

        return firstshown[0]
    
    """
    Find the next unwatched episode of a show

    If it's a plex based show, see if we need to rewind the unwatched counter
    """
    def fetchNextEpisode(self, show):
        cursor = self.connection.cursor()
        links_sql = "SELECT * FROM links WHERE show = %s"
        cursor.execute(links_sql, (show.showid,))

        lastwatchedid = self.lastWatched(show.showid)
        nextepisode = None
        
        alllinks= cursor.fetchall()
        for row in alllinks:
            if row[0] > lastwatchedid:
                nextepisode = NextEpisode(row[0], row[2], row[3])
                break

        firstepisode = -1 if show.plexname else self.firstEpisode(show.showid)
        nextepisodeid = nextepisode.linkid if nextepisode else firstepisode
            
        lastshown_sql = "UPDATE lastshown SET lastid = %s WHERE show = %s"
        cursor.execute(lastshown_sql, (nextepisodeid, show.showid,))
        self.connection.commit()

        return nextepisode

"""
Representation of a show from the database
"""
class ShowEntity():
    showid = None
    plexname = None
    showlength = None
    showtype = None
    hasexternal = False
    lastshown = -1
    
    def __init__(self, showid, showlength, showtype="tv", plexname=None, hasexternal=False, lastshown=-1):
        self.showid = showid
        self.plexname = plexname
        self.showlength = showlength
        self.showtype = showtype
        self.hasexternal = hasexternal
        self.lastshown = lastshown

"""
The next episode object used by the player
"""
class NextEpisode():
    linkid = None
    linktype = None
    uri = None

    def __init__(self, linkid, linktype, uri):
        self.linkid = linkid
        self.linktype = linktype
        self.uri = uri

