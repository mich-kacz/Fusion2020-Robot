#import sqlite3
import pymysql

def main(args=None):
    try:
        connection=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        print('Data base was opened succesfully')
    except:
        print('Data base was opened unsuccesfully')

    conn=connection.cursor() 

    #conn.execute('DROP TABLE AUTO_LOGS')

    conn.execute('''CREATE TABLE AUTO_LOGS(NR INT PRIMARY KEY NOT NULL, FRAME INT, LANES INT, F_SENS INT, DATE TIMESTAMP DEFAULT(CURRENT_TIMESTAMP))''')
    conn.execute("INSERT INTO AUTO_LOGS VALUES(0, 10000, 0, 50, CURRENT_TIMESTAMP)")
    conn.execute("INSERT INTO AUTO_LOGS VALUES(1, 11000, 0, 51, CURRENT_TIMESTAMP)")
    conn.execute("INSERT INTO AUTO_LOGS VALUES(2, 12000, 0, 52, CURRENT_TIMESTAMP)")



    conn.execute('''CREATE TABLE MANUAL_LOGS(NR INT PRIMARY KEY NOT NULL, FRAME INT,DATE TIMESTAMP DEFAULT(CURRENT_TIMESTAMP))''')
    
    text=conn.execute("SELECT * FROM AUTO_LOGS")
    print (text)
    numb=conn.execute("SELECT COUNT(NR) FROM AUTO_LOGS")
    print('\nNumber of elements:\t')
    print(numb)

    connection.commit()
    connection.close()

if __name__=='__main__':
    main()
