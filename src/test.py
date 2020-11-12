import json
import os
import sqlite3 as lite
import sys

DB_dir='/media/dev/Data/Doan/fashion-dataset/styles'

# with open('/media/dev/Data/Doan/fashion-dataset/styles/1163.json') as json_file:
#     data = json.load(json_file)
#     p =data['data']
#     q= p['id']
#     price = p['price']
#     styleimage = p['styleImages']['search']['imageURL']
  

con= lite.connect('data.db')

for root, _, files in os.walk(DB_dir, topdown=False):
    cls = root.split('/')[-1]
    for name in files:
        if not name.endswith('.json'):
            continue
        json_link = os.path.join(root, name)
        try:
            with open(json_link) as json_file:
                data = json.load(json_file)
                p =data['data']
                name = p['productDisplayName']   
                id= p['id']
                link = str(id)+'.jpg'
                price = str(p['price'])
                linkweb = p['styleImages']['search']['imageURL']
                querry = '''
                UPDATE products SET linkweb = '{}', price = {}  
                WHERE link = '{}'
                '''.format(linkweb,price,link)
                con.execute(querry)
                con.commit()
        except:
            print (json_file)
    
         
