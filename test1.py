import psycopg2
import numpy as np

conn = psycopg2.connect("dbname=andrea user=andrea")

cur = conn.cursor()

cur.execute("SELECT * FROM autdbwiki;")
x = cur.fetchall()
print np.shape(x)

#y = [d[0] for d in cur.description]
#print y

z = cur.description
print z
