import psycopg2
import csv
import sys

# Sample record
# misterrogers	https://www.youtube.com/watch?v=Q8vj9OBx5II	youtube	tv	30    Mister Rogers

def connectToDb():
    try:
        connection = psycopg2.connect(user = "automommy",
                                      password = "automommy",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "automommy")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        return connection
    
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def closeConnection(connection):
    #closing database connection.
    if(connection):
        connection.close()
        print("PostgreSQL connection is closed")


def loadShows(connection, shows):
    with open(shows) as showsStream:
        reader = csv.reader(showsStream, delimiter='\t')
        for row in reader:
            print(row)
            showid = addShow(row, connection)
            linkid = -1
            if row[2].lower() != 'plex':
                linkid = addLink(row, showid, connection)
            addLastShown(showid, linkid, connection)

def addShow(show, connection):
    cursor = connection.cursor()
    insert_show_sql = """ INSERT INTO shows (name, showtype, showlength) VALUES (%s, %s, %s) ON CONFLICT("name") DO UPDATE SET name=EXCLUDED.name RETURNING showid """
    record = (show[0], show[3], show[4])
    cursor.execute(insert_show_sql, record)
    connection.commit()
    showid = cursor.fetchone()[0]

    print("Show id ", showid)

    if show[2].lower() == 'plex':
        update_plex_name_sql = """ UPDATE shows SET plexname = %s WHERE showid = %s"""
        cursor.execute(update_plex_name_sql, (show[5], showid))
        connection.commit()
    
    return showid

def addLink(show, showid, connection):
    cursor = connection.cursor()
    insert_link_sql = """ INSERT INTO links (show, linktype, uri) VALUES (%s, %s, %s) ON CONFLICT("uri") DO UPDATE SET uri=EXCLUDED.uri RETURNING linkid"""
    record = (showid, show[2], show[1])
    cursor.execute(insert_link_sql, record)
    connection.commit()
    linkid = cursor.fetchone()[0]

    print("Link id ", linkid)

    return linkid

def addLastShown(showid, linkid, connection):
    cursor = connection.cursor()
    insert_last_sql = """ INSERT INTO lastshown (show, lastid) VALUES (%s, %s) ON CONFLICT("show") DO NOTHING """
    record = (showid, linkid)
    cursor.execute(insert_last_sql, record)
    connection.commit()
    
if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Missing argument, the file with the shows")
        sys.exit(-1)

    showsFile = sys.argv[1]
    
    connection = connectToDb()

    loadShows(connection, showsFile)
    closeConnection(connection)
