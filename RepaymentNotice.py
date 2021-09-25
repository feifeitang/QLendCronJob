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
        print('expire in %s days:' % day)
        print('have %s repaymentRecords' % len(repaymentRecords))
        for index, repaymentRecord in enumerate(repaymentRecords):
            if len(repaymentRecords) > 1 and index != 0:
                print('-----next record-----')
            repaymentNumber = repaymentRecord[0]
            loanNumber = repaymentRecord[1]

            foreignWorkerId = getLoanRecordByLoanNumber(loanNumber)

            print('foreignWorkerId: {0}\nrepaymentNumber: {1}\nloanNumber: {2}'.format(foreignWorkerId, repaymentNumber, loanNumber))

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

            res = requests.post(url=requestUrl, headers=header, json=data)
            print('response code: ', res.status_code)

            conn.commit()
            print()

        print("finish", str(datetime.now()))

    except Exception as e:
        print("errro msg", e)
        conn.close()

def start():
    startByDay(7)
    print('-------------------------------------------')
    startByDay(3)
    print('-------------------------------------------')
    startByDay(1)
    print('-------------------------------------------')