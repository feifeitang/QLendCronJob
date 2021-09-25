import pymssql
from datetime import datetime
import requests

conn = pymssql.connect(server='34.97.221.65',
                       port='11433',
                       user='sa',
                       password='Abcd1234_@#Abcd1234_@#',
                       database='QLendDB')

requestUrl = 'https://qlend-sandbox.azurewebsites.net/api/Notifications/requests'
header = {'Content-Type': 'application/json'}


def buildNoticeContent(date):
    return 'Your repayment will expired in %s days.' % date


def getRepaymentRecordsByDate(conn, date):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = %s;',
        date)

    if cursor != None:
        return cursor.fetchall()

    return []


def getLoanRecordByLoanNumber(loanNumber):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = %s;',
        loanNumber)

    if cursor != None:
        return cursor.fetchone()[0]

    return None


def getDeviceTagByForeignWorkerId(id):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT DeviceTag FROM [QLendDB].[dbo].[ForeignWorker] WHERE ID = %s;',
        id)

    if cursor != None:
        return cursor.fetchone()[0]

    return None


def insertNotice(content, foreignWorkerId):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'{0}\', 0, \'RepaymentDetailPage\', GETDATE(), {1});'
        .format(content, foreignWorkerId))


def start():
    try:
        RepaymentRecord_cursor = conn.cursor()
        LoanRecord_cursor = conn.cursor()
        Notice_cursor = conn.cursor()
        ForeignWorker_cursor = conn.cursor()

        # expire in 7 days
        RepaymentRecord_cursor.execute(
            'SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 7;'
        )
        repaymentRecords = RepaymentRecord_cursor.fetchone()
        print('expire in 7 days:')
        while repaymentRecords:
            repaymentNumber = str(repaymentRecords[0])
            loanNumber = str(repaymentRecords[1])
            print('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' +
                  loanNumber)

            LoanRecord_cursor.execute(
                'SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'
                .format(loanNumber))

            foreignWorkerId = getLoanRecordByLoanNumber(loanNumber)
            print('foreignWorkerId: ', foreignWorkerId)

            content = 'Your repayment will expired in 7 days.'
            Notice_cursor.execute(
                'INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'{0}\', 0, \'RepaymentDetailPage\', GETDATE(), {1});'
                .format(content, foreignWorkerId))

            ForeignWorker_cursor.execute(
                'SELECT DeviceTag FROM [QLendDB].[dbo].[ForeignWorker] WHERE ID = {0}'
                .format(foreignWorkerId))
            deviceTag = str((ForeignWorker_cursor.fetchone())[0])

            data = {
                "title": "QLend",
                "text": content,
                "action": content,
                "tags": deviceTag,
                "silent": False
            }

            print('data', data)

            res = requests.post(requestUrl, header, json=data)
            print(res.status_code)

            repaymentRecords = RepaymentRecord_cursor.fetchone()

            conn.commit()

        print()

        # expire in 3 days
        repaymentRecords = getRepaymentRecordsByDate(conn, 3)
        print('get repaymentRecords', repaymentRecords)
        print('expire in 3 days:')
        for repaymentRecord in repaymentRecords:
            repaymentNumber = str(repaymentRecord[0])
            loanNumber = str(repaymentRecord[1])
            print('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' +
                  loanNumber)

            LoanRecord_cursor.execute(
                'SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'
                .format(loanNumber))

            foreignWorkerId = getLoanRecordByLoanNumber(loanNumber)
            print('foreignWorkerId: ', foreignWorkerId)

            content = buildNoticeContent(3)

            insertNotice(content, foreignWorkerId)

            deviceTag = [getDeviceTagByForeignWorkerId(foreignWorkerId)]

            data = {
                "title": "QLend",
                "text": content,
                "action": content,
                "tags": deviceTag,
                "silent": False
            }

            print('data', data)

            res = requests.post(url=requestUrl, headers=header, json=data)
            print('response code: ', res.status_code)
            print('response data: ', res.text)

            conn.commit()

        print()

        # expire in 1 days
        RepaymentRecord_cursor.execute(
            'SELECT RepaymentNumber, LoanNumber FROM [QLendDB].[dbo].[RepaymentRecord] WHERE DATEDIFF(day, GETDATE(), RepaymentDate) = 1;'
        )
        repaymentRecords = RepaymentRecord_cursor.fetchone()
        print('expire in 1 days:')
        while repaymentRecords:
            repaymentNumber = str(repaymentRecords[0])
            loanNumber = str(repaymentRecords[1])
            print('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' +
                  loanNumber)

            LoanRecord_cursor.execute(
                'SELECT ID FROM [QLendDB].[dbo].[LoanRecord] WHERE LoanNumber = \'{0}\';'
                .format(loanNumber))
            foreignWorkerId = str((LoanRecord_cursor.fetchone())[0])
            print('foreignWorkerId: ' + foreignWorkerId)

            repaymentRecords = RepaymentRecord_cursor.fetchone()

            print('repaymentRecords', repaymentRecords)

            Notice_cursor.execute(
                'INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'Your repayment will expired in 1 days.\', 0, \'RepaymentDetailPage\', GETDATE(), {0});'
                .format(foreignWorkerId))
            conn.commit()

        print("finish", str(datetime.now()))

    except Exception as e:
        print("errro msg", e)
        conn.close()
