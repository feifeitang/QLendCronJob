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


def startByDay(day):
    try:
        repaymentRecords = getRepaymentRecordsByDate(conn, day)
        print('get repaymentRecords', repaymentRecords)
        print('expire in %s days:' % day)
        for repaymentRecord in repaymentRecords:
            print(type (repaymentRecord[0]))
            repaymentNumber = str(repaymentRecord[0])
            loanNumber = str(repaymentRecord[1])
            print('repaymentNumber: ' + repaymentNumber + 'loanNumber: ' +
                  loanNumber)

            foreignWorkerId = getLoanRecordByLoanNumber(loanNumber)
            print('foreignWorkerId: ', foreignWorkerId)

            content = buildNoticeContent(day)

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

            conn.commit()

        print("finish", str(datetime.now()))

    except Exception as e:
        print("errro msg", e)
        conn.close()
