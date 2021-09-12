import time
import RepaymentNotice

def setInterval(func, sec):
    func()
    time.sleep(sec)
    setInterval(func, sec)

try:
    setInterval(RepaymentNotice.start, 86400)
except Exception as e:
    print('main error', e)

