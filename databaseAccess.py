import pymssql
conn = pymssql.connect(server='srvEXT',user='sa', password='senhasa@1234', database='SimplesADM')
cursor = conn.cursor()
cursor.execute("select * from dbo.produto where lojcod = 20 and procod =2000 ")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))
    row = cursor.fetchone()
conn.close()
