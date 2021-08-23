import pymssql

conn = pymssql.connect(
    server = '34.97.221.65',
    # post = '11433',
    user= 'sa',
    password='Abcd1234_@#Abcd1234_@#',
    database='QLendDB'
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 7;')
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
    row = cursor.fetchone()