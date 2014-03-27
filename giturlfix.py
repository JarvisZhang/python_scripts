'''
    update url from 
        https://code.engineering.redhat.com/gerrit/p/<project>.git
    to
        https://code.engineering.redhat.com/gerrit/<project>.git
'''
import MySQLdb

MySQL_SETTINGS = {
    'host': 'localhost',
    'user': 'root',
    'db': 'gitview',
    'passwd': ''
}


if __name__ == "__main__":
    try:
        conn = MySQLdb.connect(
            host = MySQL_SETTINGS['host'],
            user = MySQL_SETTINGS['user'],
            passwd = MySQL_SETTINGS['passwd'],
            db = MySQL_SETTINGS['db']
        )
        cur= conn.cursor()
        cur.execute('select id, url from viewapp_project')
        projects = list(cur.fetchall())
        for project in projects:
            url_new = project[1].replace('/p/', '/')
            if url_new != project[1]:
                sql = 'update viewapp_project set url = "%s" where id = %d' % (url_new, int(project[0]))
                print sql
                cur.execute(sql)
            conn.commit()
        print "URL UPDATE FINISH!"
    except MySQLdb.Error, e:
        print 'MySQL Error %d: %s' %(e.args[0], e.args[1])
