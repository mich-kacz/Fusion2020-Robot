import sqlite3

def main(args=None):
    try:
        conn=sqlite3.connect('auto_logs.db')
        print('Data base was opened succesfully')
    except:
        print('Data base was opened unsuccesfully')
    #conn.execute('DROP TABLE AUTO_LOGS')
    #conn.execute('''CREATE TABLE AUTO_LOGS (
    #        NR INT PRIMARY KEY NOT NULL,
    #        FRAME INT,
    #        LINES SMALL INT,
    #        F_SENS INT)''')
    #conn.execute("INSERT INTO AUTO_LOGS VALUES(0, 10000, 0, 50)")
    #conn.execute("INSERT INTO AUTO_LOGS VALUES(1, 11000, 0, 51)")
    #conn.execute("INSERT INTO AUTO_LOGS VALUES(2, 12000, 0, 52)")

    for row in conn.execute("SELECT* FROM AUTO_LOGS"):
        print (row)
    numb=conn.execute("SELECT COUNT(NR) FROM AUTO_LOGS")
    print('\nNumber of elements:\t')
    print(numb.fetchall()[0][0])

    conn.commit()
    conn.close()

if __name__=='__main__':
    main()
