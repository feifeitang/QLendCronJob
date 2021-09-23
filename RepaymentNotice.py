import pymssql
from datetime import datetime

conn = pymssql.connect(
    server = '34.97.221.65',
    port = '11433',
    user= 'sa',
    password='Abcd1234_@#Abcd1234_@#',
    database='QLendDB'
)

def start():
    try:
        RepaymentRecord_cursor = conn.cursor()
        LoanRecord_cursor = conn.cursor()
        Notice_cursor = conn.cursor()

        # expire in 7 days
        RepaymentRecord_cursor.execute('SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 7;')
        repaymentRecords = RepaymentRecord_cursor.fetchone()
        print ('expire in 7 days:')
        while repaymentRecords:
            repaymentNumber = str(repaymentRecords[0])
            loanNumber = str(repaymentRecords[1])
            print ('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' + loanNumber)

            LoanRecord_cursor.execute('SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'.format(loanNumber))
            foreignWorkerId = str((LoanRecord_cursor.fetchone())[0])
            print('foreignWorkerId: ' + foreignWorkerId)
            
            repaymentRecords = RepaymentRecord_cursor.fetchone()

            Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your repayment will expired in 7 days.\', 0, \'RepaymentDetailPage\', GETDATE(), {0});'.format(foreignWorkerId))
            conn.commit()

        print()

        # expire in 3 days
        RepaymentRecord_cursor.execute('SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 3;')
        repaymentRecords = RepaymentRecord_cursor.fetchone()
        print ('expire in 3 days:')
        while repaymentRecords:
            repaymentNumber = str(repaymentRecords[0])
            loanNumber = str(repaymentRecords[1])
            print ('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' + loanNumber)

            LoanRecord_cursor.execute('SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'.format(loanNumber))
            foreignWorkerId = str((LoanRecord_cursor.fetchone())[0])
            print('foreignWorkerId: ' + foreignWorkerId)

            repaymentRecords = RepaymentRecord_cursor.fetchone()

            Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your repayment will expired in 3 days.\', 0, \'RepaymentDetailPage\', GETDATE(), {0});'.format(foreignWorkerId))
            conn.commit()

        print()

        # expire in 1 days
        RepaymentRecord_cursor.execute('SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 1;')
        repaymentRecords = RepaymentRecord_cursor.fetchone()
        print ('expire in 1 days:')
        while repaymentRecords:
            repaymentNumber = str(repaymentRecords[0])
            loanNumber = str(repaymentRecords[1])
            print ('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' + loanNumber)

            LoanRecord_cursor.execute('SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'.format(loanNumber))
            foreignWorkerId = str((LoanRecord_cursor.fetchone())[0])
            print('foreignWorkerId: ' + foreignWorkerId)

            repaymentRecords = RepaymentRecord_cursor.fetchone()

            Notice_cursor.execute('INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your repayment will expired in 1 days.\', 0, \'RepaymentDetailPage\', GETDATE(), {0});'.format(foreignWorkerId))
            conn.commit()

        print("finish", str(datetime.now()))

    except Exception as e:
        print("start errro msg", e)
        conn.close()
