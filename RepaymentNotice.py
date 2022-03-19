import pymssql
from datetime import datetime
import requests
import json

# TODO: use config connect to db
conn = pymssql.connect(server='35.229.185.4',
                       port='11433',
                       user='sa',
                       password='MyC0m9l&xP@ssw0rd',
                       database='QLendDB')

requestUrl = 'https://sandbox-app-api.qlend.tw/api/Notifications/requests'
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


def createLink(loanNumber):
    data = {
        "page": 'RepaymentDetailPage',
        "id": loanNumber
    }

    link = json.dumps(data)

    return link


def insertNotice(content, link, foreignWorkerId):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO [QLendDB].[dbo].[Notice] (Content, Status, Link, CreateTime, ForeignWorkerId) VALUES (\'{0}\', 0, \'{1}\', GETDATE(), {2});'
        .format(content, link, foreignWorkerId))

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

            link = createLink(loanNumber)

            insertNotice(content, link, foreignWorkerId)

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