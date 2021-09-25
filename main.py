import time
import RepaymentNotice

def setInterval(func, sec, param):
    func(param)
    time.sleep(sec)
    setInterval(func, sec, param)

try:
    setInterval(RepaymentNotice.start, 86400, 7)
    setInterval(RepaymentNotice.start, 86400, 3)
    setInterval(RepaymentNotice.start, 86400, 1)
except Exception as e:
    print('main error', e)

