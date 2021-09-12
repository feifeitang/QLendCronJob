import pymssql

conn = pymssql.connect(
    server = '34.97.221.65',
    port = '11433',
    user= 'sa',
    password='Abcd1234_@#Abcd1234_@#',
    database='QLendDB'
)

RepaymentRecord_cursor = conn.cursor()
Notice_cursor = conn.cursor()

# expire in 7 days
RepaymentRecord_cursor.execute('SELECT * FROM [QLendDB].[dbo].[ForeignWorker] WHERE DATEDIFF(day, \'2000-06-25\', BirthDate) = 0;')
RepaymentRecord_row = RepaymentRecord_cursor.fetchone()
while RepaymentRecord_row:
    print (str(RepaymentRecord_row[0]) + " " + str(RepaymentRecord_row[1]))
    RepaymentRecord_row = RepaymentRecord_cursor.fetchone()

    # Notice_cursor.execute('SELECT COUNT(*)+1 FROM [QLendDB].[dbo].[Notice];')
    # Notice_row = Notice_cursor.fetchone()
    # print (type(Notice_row))
    # print (str(Notice_row[0]))

    Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your #Loan n repayment will expired in 7 days.\', 0, \'RepaymentPage or RepaymentDetailPage\', GETDATE(), 1036);')
    conn.commit()

# expire in 3 days
RepaymentRecord_cursor.execute('SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 3;')
RepaymentRecord_row = RepaymentRecord_cursor.fetchone()
while RepaymentRecord_row:
    print (str(RepaymentRecord_row[0]) + " " + str(RepaymentRecord_row[1]))
    RepaymentRecord_row = RepaymentRecord_cursor.fetchone()

    # Notice_cursor.execute('SELECT COUNT(*)+1 FROM [QLendDB].[dbo].[Notice];')
    # Notice_row = Notice_cursor.fetchone()
    # print (str(Notice_row[0]))

    Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your #Loan n repayment will expired in 3 days.\', 0, \'RepaymentPage or RepaymentDetailPage\', GETDATE(), 1036);')
    conn.commit()

# expire in 1 days
RepaymentRecord_cursor.execute('SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 1;')
RepaymentRecord_row = RepaymentRecord_cursor.fetchone()
while RepaymentRecord_row:
    print (str(RepaymentRecord_row[0]) + " " + str(RepaymentRecord_row[1]))
    RepaymentRecord_row = RepaymentRecord_cursor.fetchone()

    # Notice_cursor.execute('SELECT COUNT(*)+1 FROM [QLendDB].[dbo].[Notice];')
    # Notice_row = Notice_cursor.fetchone()
    # print (str(Notice_row[0]))

    Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your #Loan n repayment will expired in 1 days.\', 0, \'RepaymentPage or RepaymentDetailPage\', GETDATE(), 1036);')
    conn.commit()

RepaymentRecord_cursor.close()
Notice_cursor.close()
conn.close()