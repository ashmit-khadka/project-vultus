import psycopg2


def query(query, Ftype):
    try:
        cs = "dbname=%s user=%s password=%s host=%s port=%s" % ("project-vultus","postgres","54321","localhost","5432")
        conn = psycopg2.connect(cs)
        cur = conn.cursor()
        cur.execute(query)
        if Ftype == 'execute':
            conn.commit()
            return None
        if Ftype == 'fetchone':
            return cur.fetchone()
        return cur.fetchall()
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)     

    finally:
        #closing database connection.
        if(conn):
            cur.close()
            conn.close()
            #print("PostgreSQL connection is closed")


#print(query("INSERT INTO content VALUES('Ati Bho','https://i.ytimg.com/vi/_dxNxNOy8hw/hqdefault.jpg','E');", 'execute'))

