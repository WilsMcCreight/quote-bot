import os
import pandas as pd
from sqlite3 import connect, Error
import sys

def run_commit(sql,conn,curs):
    try:
        curs.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def creat_tQuote(conn, curs):
    sql = """ CREATE TABLE IF NOT EXISTS tQuote (
                id integer PRIMARY KEY,
                logger_name text NOT NULL,
                quotee_name text,
                quote text NOT NULL,
                context text,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            ); """
    run_commit(sql, conn, curs)

def build_tables(conn, curs):
    # run_commit('PRAGMA foreign_keys=ON', conn, curs) # Only necessary if using multiple tables that reference each other
    creat_tQuote(conn, curs)

def connect_db(db_name):
    try:
        conn = connect(db_name)
    except Error as e:
        print(e)
        return None
    return conn

def backup_log(quote):
    with open("backup_log.txt", "a") as f:
        f.write(str(quote) + '\n')

def insert_quote(conn, curs, quote):
    sql = ''' INSERT INTO tQuote(logger_name,quotee_name,quote,context)
              VALUES(?,?,?,?)'''
    try:
        curs.execute(sql, quote)
        # curs.execute('INSERT INTO tQuote (LastModifiedTime) VALUES(CURRENT_TIMESTAMP)')
        conn.commit()
    except Error as e:
        print(e)
    backup_log(quote)
    return curs.lastrowid

def insert_quote_small(conn, curs, quote):
    sql = ''' INSERT INTO tQuote(logger_name,quote)
              VALUES(?,?)'''
    try:
        curs.execute(sql, quote)
        # curs.execute('INSERT INTO tQuote (LastModifiedTime) VALUES(CURRENT_TIMESTAMP)')
        conn.commit()
    except Error as e:
        print(e)
    backup_log(quote)
    return curs.lastrowid

if __name__ == "__main__":
    commands = ['-h', '-help', '-rb', '-rebuild', '-v', '-view', '-t', '-test']
    if len(sys.argv) != 2:
        print("Error: please input at least one command. Input command 'help' for a list of commands")
    elif sys.argv[1] not in commands:
        print("Error: command not recognized. Use -help for a list of possible commands")
    elif (sys.argv[1] == '-help') or (sys.argv[1] == '-h'):
        print("""Command List:
        -h, -help      :  Review command options
        -rb, -rebuild  :  DELTES and rebuilds the QuoteDB database
        -v, -view      :  Prints all entries in the database
        """)
    else:
        db_name = 'Quote.db'
        if (sys.argv[1] == '-rb') or (sys.argv[1] == '-rebuild'):
            inp = input("Are you sure you would like to delete the existing database? (Y/N): ")
            if inp.lower() == 'n':
                print('Phew, close call')
                sys.exit()
            print("Rebuilding database")
            if os.path.exists(db_name):
                os.remove(db_name)
            conn = connect_db(db_name)
            if (not conn):
                print('Failed to rebuild database, exiting')
            else:
                curs = conn.cursor()
                build_tables(conn, curs)
                print("Successfully rebuilt Quote.db database")
        elif (sys.argv[1] == '-v') or (sys.argv[1] == '-view'):
            conn = connect_db(db_name)
            if (not conn):
                print('Failed to connect to database, exiting')
            else:
                curs = conn.cursor()
                # print(pd.read_sql("SELECT * FROM sqlite_master;",conn))
                print(pd.read_sql("SELECT * FROM tQuote;",conn))
        elif(sys.argv[1] == '-t') or (sys.argv[1] == '-test'):
            conn = connect_db(db_name)
            if (not conn):
                print('Failed to connect to database, exiting')
            else:
                curs = conn.cursor()
                quote = ('Wils', 'Lee', 'Eatin ass and eatin ass', 'Triggs referring to a canibal orgy')
                print(insert_quote(conn, curs, quote))
        conn.close()
    