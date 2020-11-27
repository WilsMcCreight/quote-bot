import pandas as pd
import sqlite3

def RunCommit(sql,conn,curs):
    curs.execute(sql)
    conn.commit()

def BuildStoreDB():
    # !rm -f Quotes.db
    conn = sqlite3.connect('Quotes.db')
    curs = conn.cursor()
    curs.execute("PRAGMA foreign_keys=ON")
    conn.commit()
    
    # Create_tState(conn,curs)
    # Create_tZip(conn,curs)
    # Create_tCust(conn,curs)
    # Create_tOrder(conn,curs)
    # Create_tProd(conn,curs)
    # Create_tOrderDetail(conn,curs)
    
    conn.commit()
    
    return conn,curs

if __name__ == "__main__":
    conn,curs = BuildStoreDB()
    pd.read_sql("SELECT * FROM sqlite_master;",conn)