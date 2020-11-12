from __future__ import print_function

from DB import Database

import sqlite3 as lite
import sys

con = None

class SQLite(object):
    def __init__(self):
        self.con= lite.connect('data.db')
        self.con.execute('''CREATE TABLE IF NOT EXISTS products(
                    LINK TEXT PRIMARY KEY NOT NULL,
                    LINKWEB TEXT,
                    PRICE INT,
                    IMG TEXT NOT NULL,
                    LABLE TEXT NOT NULL,
   					ID_RES BIGINT,
   					ID_VGG BIGINT,
   					ID_HOG BIGINT,
   					ID_EDGE BIGINT,
   					ID_DAISY BIGINT
                    ) ''')


        self.con.close()
    def insertmuti(self,db):
        self.con= lite.connect('data.db')
        cur = self.con.cursor()
        data = db.get_data()
        try:
            for d in data.itertuples():
                d_img , d_cls ,d_file = getattr(d,"img"), getattr(d, "cls") ,getattr(d,"filename")
                cur.execute(''' INSERT INTO products(LINK,IMG,LABLE)
                            VALUES(?,?,?)''',(d_file,d_img,d_cls,))
            self.con.commit()
        except :
            pass
        
        self.con.close()


    def insert(self,LABLE,LINK,IMG):
        try:
            self.con= lite.connect('data.db')
            cur = self.con.cursor()

            
            cur.execute(''' INSERT INTO products(LINK,IMG,LABLE)
                            VALUES(?,?,?)''',(LINK,LABLE,IMG))
            self.con.commit()
            return cur.lastrowid
            
        except  :
            return False
    def select(self,feature,value):
        try:
            tmp ='id_'+feature
            querry = 'SELECT * FROM products WHERE {} = {}    ORDER BY LINK'.format(tmp.upper(),value)
            self.con= lite.connect('data.db')
            cur = self.con.cursor()
            cur.execute(querry)
            tmp = cur.fetchone()
            result ={
                            'lable':  tmp[1],
                            'linkweb':  tmp[8],
                            'price': tmp[9]
            }
            return  result
        except  :
            return []

            
    def update(self,link,feature,value):
        try:
            self.con= lite.connect('data.db')
            cur = self.con.cursor()
            tmp ='id_'+feature
            querry ='''UPDATE products set {}={} WHERE LINK='{}' '''.format(tmp.upper(),value,link)
            cur.execute(querry)
            self.con.commit()
            
        except  :
            return False
    
    def updateMuti(self,feature,li):
        try:
            tmp ='id_'+feature
            self.con= lite.connect('data.db')
            cur = self.con.cursor()
            for item in li :
                value = item['index']
                link = item['link']
                querry ='''UPDATE products set {}={} WHERE LINK='{}' '''.format(tmp.upper(),value,link)
                cur.execute(querry)
            self.con.commit()
            self.con.close()
            
        except  :
            return False

    def close(self):
        self.con.close()
        return True

if __name__ == '__main__':   
    db = Database()
    data = db.get_data()

    sql = SQLite()
    sql.insertmuti(db)
    sql.update('10000.jpg','res',1)
    tmp =sql.select('res',1)
    



    for d in data.itertuples():
        d_img , d_cls ,d_file = getattr(d,"img"), getattr(d, "cls") ,getattr(d,"filename")
        sql.insert(d_cls,d_file,d_img)
    sql.close()


    
        